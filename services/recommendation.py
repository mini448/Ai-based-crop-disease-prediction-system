# Fix recommendation.py properly
class RecommendationEngine:
    def __init__(self):
        self.recommendations = {
            'Bacterial_spot': {
                'preventive': [
                    'Use certified disease-free seeds and transplants',
                    'Avoid overhead irrigation - use drip irrigation',
                    'Remove and destroy infected plant debris',
                    'Practice crop rotation (3-4 years)',
                    'Ensure proper plant spacing for air circulation',
                    'Sanitize tools between plants'
                ],
                'explanation': 'Bacterial spot spreads through water splash and contaminated materials. Focus on sanitation and avoiding wet foliage.'
            },
            'Early_blight': {
                'preventive': [
                    'Rotate crops every 2-3 years',
                    'Stake or cage plants to improve air circulation',
                    'Mulch around plants to prevent soil splash',
                    'Remove lower leaves touching soil',
                    'Water at the base of plants',
                    'Maintain adequate plant nutrition'
                ],
                'explanation': 'Early blight is favored by warm, humid conditions. Proper spacing and moisture management are key.'
            },
            'Late_blight': {
                'preventive': [
                    'Plant late blight resistant varieties',
                    'Ensure good field drainage',
                    'Avoid overhead irrigation',
                    'Destroy volunteer tomatoes and potato culls',
                    'Monitor weather for blight-favorable conditions',
                    'Maintain proper plant spacing'
                ],
                'explanation': 'Late blight spreads rapidly in cool, wet weather. Early detection and prevention are critical.'
            },
            'Leaf_Mold': {
                'preventive': [
                    'Improve ventilation in greenhouse/field',
                    'Reduce humidity around plants',
                    'Avoid wetting foliage during irrigation',
                    'Space plants properly for air circulation',
                    'Remove infected leaves promptly',
                    'Use resistant varieties when available'
                ],
                'explanation': 'Leaf mold thrives in high humidity and poor air circulation. Ventilation is key.'
            }
        }
    
    def get_recommendations(self, predicted_disease, crop_name):
        if 'healthy' in predicted_disease.lower():
            return {
                'type': 'healthy',
                'message': 'Your crop appears healthy! Continue with good agricultural practices.',
                'recommendations': [
                    'Maintain proper irrigation schedule',
                    'Monitor for pests regularly',
                    'Apply balanced fertilization as per soil test',
                    'Practice crop rotation for future seasons',
                    'Keep field clean of weeds and debris'
                ],
                'explanation': 'Prevention is better than cure. Continue monitoring your crops regularly.'
            }
        
        key = predicted_disease
        if key in self.recommendations:
            rec = self.recommendations[key]
            return {
                'type': 'diseased',
                'message': f'Preventive measures for {crop_name} disease management:',
                'recommendations': rec['preventive'],
                'explanation': rec['explanation']
            }
        else:
            return {
                'type': 'general',
                'message': 'General disease management recommendations:',
                'recommendations': [
                    'Remove and destroy infected plant parts',
                    'Improve air circulation through proper spacing',
                    'Avoid overhead watering - water at soil level',
                    'Practice crop rotation',
                    'Maintain field sanitation',
                    'Monitor plants regularly for early detection',
                    'Consult local agricultural extension services for specific guidance'
                ],
                'explanation': 'Follow integrated disease management practices. For severe cases, consult agricultural experts.'
            }
