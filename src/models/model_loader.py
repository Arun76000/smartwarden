"""
Model loader for trained AI models in Smart Contract AI Analyzer.
"""

import joblib
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class ModelLoader:
    """Loads and manages trained AI models."""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models = {}
        self.metadata = None
        self.load_metadata()
    
    def load_metadata(self):
        """Load model metadata."""
        metadata_path = self.models_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            logger.info("Model metadata loaded")
        else:
            logger.warning("No model metadata found")
    
    def load_model(self, model_name: str):
        """Load a specific model."""
        if not self.metadata:
            logger.error("No metadata available")
            return None
        
        if model_name not in self.metadata['models']:
            logger.error(f"Model {model_name} not found in metadata")
            return None
        
        model_info = self.metadata['models'][model_name]
        model_path = Path(model_info['file'])
        
        if not model_path.exists():
            logger.error(f"Model file not found: {model_path}")
            return None
        
        try:
            model = joblib.load(model_path)
            self.models[model_name] = model
            logger.info(f"Model {model_name} loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return None
    
    def load_all_models(self):
        """Load all available models."""
        if not self.metadata:
            return False
        
        success = True
        for model_name in self.metadata['models'].keys():
            if not self.load_model(model_name):
                success = False
        
        return success
    
    def get_model(self, model_name: str):
        """Get a loaded model."""
        if model_name not in self.models:
            self.load_model(model_name)
        
        return self.models.get(model_name)
    
    def predict_binary(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make binary vulnerability prediction."""
        model = self.get_model('binary_classifier')
        if not model:
            return {'error': 'Binary classifier not available'}
        
        try:
            # Convert features to DataFrame
            feature_names = self.metadata['features']
            feature_values = [features.get(name, 0) for name in feature_names]
            X = pd.DataFrame([feature_values], columns=feature_names)
            
            # Make prediction
            prediction = model.predict(X)[0]
            probability = model.predict_proba(X)[0]
            
            return {
                'is_vulnerable': bool(prediction),
                'confidence': float(max(probability)),
                'probabilities': {
                    'safe': float(probability[0]),
                    'vulnerable': float(probability[1])
                }
            }
        except Exception as e:
            logger.error(f"Binary prediction failed: {e}")
            return {'error': str(e)}
    
    def predict_multiclass(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make multi-class vulnerability prediction."""
        model = self.get_model('multiclass_classifier')
        if not model:
            return {'error': 'Multi-class classifier not available'}
        
        try:
            # Convert features to DataFrame
            feature_names = self.metadata['features']
            feature_values = [features.get(name, 0) for name in feature_names]
            X = pd.DataFrame([feature_values], columns=feature_names)
            
            # Make prediction
            prediction = model.predict(X)[0]
            probabilities = model.predict_proba(X)[0]
            classes = model.classes_
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1]
            top_predictions = [
                {
                    'vulnerability_type': classes[i],
                    'confidence': float(probabilities[i])
                }
                for i in top_indices[:3]  # Top 3 predictions
            ]
            
            return {
                'predicted_type': prediction,
                'confidence': float(max(probabilities)),
                'top_predictions': top_predictions,
                'all_probabilities': {
                    classes[i]: float(probabilities[i]) 
                    for i in range(len(classes))
                }
            }
        except Exception as e:
            logger.error(f"Multi-class prediction failed: {e}")
            return {'error': str(e)}
    
    def get_feature_importance(self, model_name: str) -> Optional[Dict[str, float]]:
        """Get feature importance from a model."""
        model = self.get_model(model_name)
        if not model or not hasattr(model, 'model'):
            return None
        
        try:
            if hasattr(model.model, 'feature_importances_'):
                feature_names = self.metadata['features']
                importances = model.model.feature_importances_
                return dict(zip(feature_names, importances))
        except Exception as e:
            logger.error(f"Failed to get feature importance: {e}")
        
        return None
    
    def is_available(self) -> bool:
        """Check if models are available."""
        return (
            self.metadata is not None and 
            len(self.models) > 0 and
            self.models_dir.exists()
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        if not self.metadata:
            return {'available': False, 'error': 'No metadata'}
        
        info = {
            'available': True,
            'models_loaded': list(self.models.keys()),
            'models_available': list(self.metadata['models'].keys()),
            'created_at': self.metadata.get('created_at'),
            'features': self.metadata.get('features', [])
        }
        
        return info

# Global model loader instance
_model_loader = None

def get_model_loader() -> ModelLoader:
    """Get the global model loader instance."""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
    return _model_loader

def load_models():
    """Load all models."""
    loader = get_model_loader()
    return loader.load_all_models()

def predict_vulnerability(features: Dict[str, Any]) -> Dict[str, Any]:
    """Make vulnerability predictions using loaded models."""
    loader = get_model_loader()
    
    if not loader.is_available():
        return {
            'error': 'AI models not available',
            'available': False,
            'suggestion': 'Run: python setup_ai_models.py'
        }
    
    # Get both binary and multi-class predictions
    binary_result = loader.predict_binary(features)
    multiclass_result = loader.predict_multiclass(features)
    
    # Get feature importance
    feature_importance = loader.get_feature_importance('binary_classifier')
    
    return {
        'available': True,
        'binary_prediction': binary_result,
        'multiclass_prediction': multiclass_result,
        'feature_importance': feature_importance,
        'model_info': loader.get_model_info()
    }