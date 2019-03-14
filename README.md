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
- Labeler:
    - Speed: 108.9 s for 250 images
    - 56% accuracy within Top-5 tags
    - 46.4% accuracy with confidence > 50%
- Text Extractor:
    - Speed: 89.3s for 175 images
    - Mean Jaccard Similarity: 23.4% 
    
- Face Detection:
    - Speed: 192.9s for 550 images
    - Mean Accuracy: 99.8% 
    - Confidence score only available for certain facial features, not detection

Azure repo located [here](https://github.com/jakesingh/azure_final).

AWS Results:
- Labeler:
    - Speed: 230s for 250 images (using S3 bucket)
    - Speed: 351s for 250 images (using direct upload)
    - Mean Accuracy: 49.1%
    - Mean Accurancy (Synonyms): 78.6%
- Text Extractor:
    - Speed: 356s for 175 images (using S3 bucket)
    - Speed: 592s for 175 images (using direct upload)
    - Mean Jaccard Similarity: 48.5%
- Face Detector:
    - Speed: 645s for 550 images (using S3 bucket)
    - Speed: 957s for 550 images (using direct upload)
    - Mean Accuracy: 96.3%
