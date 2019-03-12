# Image-Identification 
## Comparing AWS, Azure, and Google Cloud Vision 

Comparison of face detection, text detection, and object tagging between three cloud service providers.

Units of comparison:
- Accuracy
- Cost
- Speed/Latency

---
Link to Paper: <i>In Progress</i>

COEN 241, Cloud Computing

Santa Clara University 

---

Google Results:
- Labeler:
    - Speed: 70.8s for 250 images
    - Mean Accuracy: 58.1%
- Text Extractor:
    - Speed: 160.7s for 175 images
    - Mean Jaccard Similarity: 45.7%
- Face Detector:
    - Speed: 303.6s for 550 images
    - Mean Accuracy: 99.8%
    
Azure Results:
- Labeling:
    - Time taken: 108.9 s
    - 56% accuracy within Top-5 tags
    - 46.4% accuracy with confidence > 50%

- Face Detection:
    - Speed: 192.9s for 550 images
    - Mean Accuracy: 99.8% 
    - No confidence score available (True/False Only)

Private Azure repo located [here](https://github.com/jakesingh/azure_final).