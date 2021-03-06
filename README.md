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
- Cost
    - Free Tier: 5000 transactions free/month, capped at 200$ credit.
    - Paid Tier: 
        - Tag, Face:
           - 0-1M transactions: $1 per 1,000 transactions                         
           - 1M-5M transactions — $0.80 per 1,000 transactions 
           - 5M-10M transactions — $0.65 per 1,000 transactions 
           - 10M-100M transactions — $0.65 per 1,000 transactions 
           - 100M+ transactions — $0.65 per 1,000 transactions 
         
         - OCR: 
             - 0-1M transactions — $1.50 per 1,000 transactions 
             - 1M-5M transactions — $1 per 1,000 transactions 
             - 5M-10M transactions — $0.65 per 1,000 transactions 
             - 10M-100M transactions — $0.65 per 1,000 transactions 
             - 100M+ transactions — $0.65 per 1,000 transactions 
         
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

More can be located [here](https://github.com/jakesingh/azure_final).

AWS Results:
- Cost
    - FreeTier: 5000 images/month
    - PaidTier: 
         - $1 per 1000 images for first 1Million images
         - $.80 per 1000 images for next 9Million images
         - $.60 per 1000 images for next 90Million images
         - $.40 per 1000 images if over 100Million images 
- Labeler:
    - Speed: 230s for 250 images (using S3 bucket)
    - Speed: 351s for 250 images (using direct upload)
    - Mean Accuracy: 58.0%
    - Mean Accuracy: 49.1% (Raw without lemmatize)
    - Mean Accurancy (Synonyms): 78.6%
- Text Extractor:
    - Speed: 356s for 175 images (using S3 bucket)
    - Speed: 592s for 175 images (using direct upload)
    - Mean Jaccard Similarity: 48.5%
- Face Detector:
    - Speed: 645s for 550 images (using S3 bucket)
    - Speed: 957s for 550 images (using direct upload)
    - Mean Accuracy: 96.3%
