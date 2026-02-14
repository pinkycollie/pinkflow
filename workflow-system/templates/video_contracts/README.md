# Video Contract Templates

This directory contains sign language video templates for FastDoc document rendering.

## Template Structure

Templates are organized by document type and sign language:

```
video_contracts/
├── asl/                    # American Sign Language
│   ├── contract.json       # Contract template metadata
│   ├── agreement.json      # Agreement template metadata
│   └── consent_form.json   # Consent form template metadata
├── bsl/                    # British Sign Language
│   └── ...
├── assets/                 # Shared video assets
│   ├── intro.mp4           # Standard introduction
│   ├── outro.mp4           # Standard closing
│   └── backgrounds/        # Background images
└── README.md               # This file
```

## Template Metadata Format

Each template JSON file contains:

```json
{
    "template_id": "contract_asl_v1",
    "name": "Standard Contract",
    "language": "ASL",
    "version": "1.0.0",
    "duration_estimate": 180,
    "sections": [
        {
            "id": "intro",
            "name": "Introduction",
            "asset": "assets/intro.mp4",
            "duration": 10
        },
        {
            "id": "content",
            "name": "Contract Content",
            "type": "dynamic",
            "placeholder": true
        },
        {
            "id": "signature_prompt",
            "name": "Signature Request",
            "asset": "signature_prompt.mp4",
            "duration": 15
        }
    ],
    "settings": {
        "resolution": "1280x720",
        "framerate": 30,
        "background_color": "#FFFFFF",
        "text_position": "bottom"
    }
}
```

## Creating New Templates

1. Create a new JSON file with template metadata
2. Add any required video assets to the assets directory
3. Register the template with the FastDoc system

## Supported Sign Languages

- **ASL** - American Sign Language
- **BSL** - British Sign Language  
- **Auslan** - Australian Sign Language
- **LSF** - French Sign Language
- **DGS** - German Sign Language

## Accessibility Guidelines

Templates should follow these accessibility guidelines:

1. **Clear signing**: Ensure signer is clearly visible with good lighting
2. **Appropriate pacing**: Allow time for comprehension
3. **Consistent framing**: Maintain consistent camera angle
4. **High contrast**: Use backgrounds that provide good contrast
5. **Caption support**: Include text captions where appropriate
