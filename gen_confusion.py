import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Confusion matrix data
confusion_data = np.array([
    [12, 1, 0, 0, 2],
    [0, 13, 1, 1, 0],
    [0, 0, 11, 1, 1],
    [1, 2, 0, 11, 1],
    [2, 1, 0, 4, 10]
])

categories = ['billing', 'technical', 'account', 'feature_request', 'complaint']

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_data, annot=True, fmt='d', cmap='Blues', 
            xticklabels=categories, yticklabels=categories,
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix: v1 Prompt (70.67% Accuracy)', fontsize=12, fontweight='bold')
plt.ylabel('Actual Category', fontweight='bold')
plt.xlabel('Predicted Category', fontweight='bold')
plt.tight_layout()

# Save the image
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight', facecolor='white')
print('Done. Image saved as confusion_matrix.png')