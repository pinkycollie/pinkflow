"""
Tests for FastDoc module functionality.
Run with: python3 test_fastdoc.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.fastdoc import (
    FFmpegAdapter,
    VideoConfig,
    VideoResolution,
    VideoCodec,
    QRGenerator,
    QRCodeConfig,
    QRErrorCorrectionLevel,
    VCodeIntegration,
    SignerInfo,
    SignerRole,
    VerificationLevel,
    SignatureStatus,
    NotaryWorkflowOrchestrator,
    DocumentType,
    NotaryWorkflowStatus
)


def test_ffmpeg_adapter_initialization():
    """Test FFmpeg adapter initialization."""
    print("Testing FFmpeg adapter initialization...")
    
    adapter = FFmpegAdapter()
    assert adapter.ffmpeg_path == "ffmpeg"
    assert adapter.temp_dir == "/tmp/fastdoc"
    assert adapter.max_duration == 600
    
    # Test with custom config
    adapter = FFmpegAdapter({
        'ffmpeg_path': '/usr/local/bin/ffmpeg',
        'max_duration': 300
    })
    assert adapter.ffmpeg_path == '/usr/local/bin/ffmpeg'
    assert adapter.max_duration == 300
    
    print("✓ FFmpeg adapter initialization test passed")


def test_video_config():
    """Test video configuration."""
    print("Testing video configuration...")
    
    config = VideoConfig()
    assert config.resolution == VideoResolution.HD
    assert config.codec == VideoCodec.H264
    assert config.framerate == 30
    
    config_dict = config.to_dict()
    assert config_dict['resolution'] == "1280x720"
    assert config_dict['codec'] == "libx264"
    
    print("✓ Video configuration test passed")


def test_render_job_creation():
    """Test render job creation."""
    print("Testing render job creation...")
    
    adapter = FFmpegAdapter()
    job = adapter.create_render_job(
        contract_id="contract_001",
        input_path="/tmp/input.mp4",
        output_path="/tmp/output.mp4",
        metadata={'test': True}
    )
    
    assert job.contract_id == "contract_001"
    assert job.input_path == "/tmp/input.mp4"
    assert job.output_path == "/tmp/output.mp4"
    assert job.status == "pending"
    assert job.metadata['test'] == True
    
    # Verify job is stored
    assert adapter.get_job_status(job.job_id) is not None
    
    print("✓ Render job creation test passed")


def test_contract_video_render():
    """Test contract video rendering."""
    print("Testing contract video rendering...")
    
    adapter = FFmpegAdapter()
    result = adapter.render_contract_video(
        contract_id="contract_002",
        contract_content="This is a test contract content.",
        output_path="/tmp/fastdoc/output/contract_002.mp4"
    )
    
    assert result['success'] == True
    assert result['contract_id'] == "contract_002"
    assert 'job_id' in result
    
    print("✓ Contract video rendering test passed")


def test_qr_generator_initialization():
    """Test QR generator initialization."""
    print("Testing QR generator initialization...")
    
    generator = QRGenerator()
    assert generator.base_url == "https://fastdoc.example.com/video"
    assert generator.default_expiration_days == 365
    
    generator = QRGenerator({
        'base_url': 'https://custom.example.com',
        'signing_key': 'test_key'
    })
    assert generator.base_url == 'https://custom.example.com'
    assert generator.signing_key == 'test_key'
    
    print("✓ QR generator initialization test passed")


def test_qr_code_generation():
    """Test QR code generation."""
    print("Testing QR code generation...")
    
    generator = QRGenerator({'signing_key': 'test_key_123'})
    
    qr_code = generator.generate_qr_code(
        document_id="doc_001",
        video_url="https://example.com/video/doc_001",
        metadata={'version': '1.0'}
    )
    
    assert qr_code.document_id == "doc_001"
    assert qr_code.data.video_url == "https://example.com/video/doc_001"
    assert qr_code.data.signature is not None
    assert qr_code.image_base64 is not None
    
    # Verify signature
    assert generator.verify_signature(qr_code.data) == True
    
    print("✓ QR code generation test passed")


def test_batch_qr_generation():
    """Test batch QR code generation."""
    print("Testing batch QR code generation...")
    
    generator = QRGenerator()
    
    documents = [
        {'document_id': 'doc_001', 'metadata': {'type': 'contract'}},
        {'document_id': 'doc_002', 'metadata': {'type': 'agreement'}},
        {'document_id': 'doc_003', 'video_url': 'https://custom.url/video'}
    ]
    
    qr_codes = generator.batch_generate(documents)
    
    assert len(qr_codes) == 3
    assert qr_codes[0].document_id == 'doc_001'
    assert qr_codes[2].data.video_url == 'https://custom.url/video'
    
    print("✓ Batch QR generation test passed")


def test_vcode_integration_initialization():
    """Test vCODE integration initialization."""
    print("Testing vCODE integration initialization...")
    
    vcode = VCodeIntegration()
    assert vcode.pinksync_url == "https://pinksync.example.com"
    assert vcode.default_expiration_hours == 72
    assert vcode.enable_notifications == True
    
    vcode = VCodeIntegration({
        'pinksync_url': 'https://custom.pinksync.com',
        'enable_notifications': False
    })
    assert vcode.pinksync_url == 'https://custom.pinksync.com'
    assert vcode.enable_notifications == False
    
    print("✓ vCODE integration initialization test passed")


def test_signing_request_creation():
    """Test signing request creation."""
    print("Testing signing request creation...")
    
    vcode = VCodeIntegration({'enable_notifications': False})
    
    signers = [
        SignerInfo(
            signer_id="signer_001",
            name="John Doe",
            email="john@example.com",
            role=SignerRole.PRIMARY
        ),
        SignerInfo(
            signer_id="signer_002",
            name="Jane Smith",
            email="jane@example.com",
            role=SignerRole.WITNESS
        )
    ]
    
    request = vcode.create_signing_request(
        document_id="doc_001",
        document_title="Test Contract",
        video_url="https://example.com/video/doc_001",
        signers=signers,
        verification_level=VerificationLevel.NOTARY
    )
    
    assert request.document_id == "doc_001"
    assert request.document_title == "Test Contract"
    assert len(request.signers) == 2
    assert request.status == SignatureStatus.PENDING
    assert request.verification_level == VerificationLevel.NOTARY
    assert len(request.audit_trail) == 1
    
    print("✓ Signing request creation test passed")


def test_signature_capture():
    """Test signature capture workflow."""
    print("Testing signature capture workflow...")
    
    vcode = VCodeIntegration({'enable_notifications': False})
    
    signers = [
        SignerInfo(signer_id="signer_001", name="John Doe")
    ]
    
    request = vcode.create_signing_request(
        document_id="doc_002",
        document_title="Test Agreement",
        video_url="https://example.com/video/doc_002",
        signers=signers
    )
    
    # Capture signature
    result = vcode.capture_signature(
        request_id=request.request_id,
        signer_id="signer_001",
        video_url="https://storage.example.com/signatures/sig_001.mp4",
        duration=15.5,
        ip_address="192.168.1.1"
    )
    
    assert result['success'] == True
    assert 'signature_id' in result
    assert result['request_complete'] == True
    
    # Verify request is now signed
    updated_request = vcode.get_signing_request(request.request_id)
    assert updated_request['status'] == 'signed'
    
    print("✓ Signature capture workflow test passed")


def test_signature_verification():
    """Test signature verification."""
    print("Testing signature verification...")
    
    vcode = VCodeIntegration({'enable_notifications': False})
    
    signers = [SignerInfo(signer_id="signer_001", name="John Doe")]
    request = vcode.create_signing_request(
        document_id="doc_003",
        document_title="Verification Test",
        video_url="https://example.com/video/doc_003",
        signers=signers
    )
    
    # Capture signature
    capture_result = vcode.capture_signature(
        request_id=request.request_id,
        signer_id="signer_001",
        video_url="https://storage.example.com/signatures/sig_002.mp4",
        duration=10.0
    )
    
    signature_id = capture_result['signature_id']
    
    # Verify signature
    verify_result = vcode.verify_signature(signature_id, "notary_001")
    
    assert verify_result['success'] == True
    assert verify_result['hash_valid'] == True
    assert verify_result['verified_at'] is not None
    
    print("✓ Signature verification test passed")


def test_notary_workflow_orchestrator():
    """Test notary workflow orchestrator initialization."""
    print("Testing notary workflow orchestrator...")
    
    orchestrator = NotaryWorkflowOrchestrator()
    
    assert orchestrator.ffmpeg is not None
    assert orchestrator.qr_generator is not None
    assert orchestrator.vcode is not None
    
    print("✓ Notary workflow orchestrator test passed")


def test_create_notary_workflow():
    """Test creating a notary workflow."""
    print("Testing notary workflow creation...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [
        SignerInfo(signer_id="party_a", name="Party A"),
        SignerInfo(signer_id="party_b", name="Party B", role=SignerRole.COUNTER_PARTY)
    ]
    
    workflow = orchestrator.create_workflow(
        document_id="contract_001",
        title="Service Agreement",
        content="This agreement is made between Party A and Party B...",
        document_type=DocumentType.CONTRACT,
        created_by="admin",
        signers=signers,
        verification_level=VerificationLevel.NOTARY
    )
    
    assert workflow.document.document_id == "contract_001"
    assert workflow.document.title == "Service Agreement"
    assert workflow.document.document_type == DocumentType.CONTRACT
    assert workflow.status == NotaryWorkflowStatus.DRAFT
    assert len(workflow.signers) == 2
    assert len(workflow.audit_trail) == 1
    
    print("✓ Notary workflow creation test passed")


def test_workflow_video_rendering():
    """Test workflow video rendering step."""
    print("Testing workflow video rendering...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [SignerInfo(signer_id="signer", name="Signer")]
    workflow = orchestrator.create_workflow(
        document_id="doc_video",
        title="Video Test",
        content="Test content",
        document_type=DocumentType.AGREEMENT,
        created_by="admin",
        signers=signers
    )
    
    result = orchestrator.render_video(workflow.workflow_id)
    
    assert result['success'] == True
    
    # Check workflow was updated
    updated = orchestrator.get_workflow(workflow.workflow_id)
    assert updated['video_url'] is not None
    assert updated['video_rendered_at'] is not None
    
    print("✓ Workflow video rendering test passed")


def test_workflow_qr_generation():
    """Test workflow QR code generation step."""
    print("Testing workflow QR generation...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [SignerInfo(signer_id="signer", name="Signer")]
    workflow = orchestrator.create_workflow(
        document_id="doc_qr",
        title="QR Test",
        content="Test content",
        document_type=DocumentType.AGREEMENT,
        created_by="admin",
        signers=signers
    )
    
    # First render video
    orchestrator.render_video(workflow.workflow_id)
    
    # Then generate QR
    result = orchestrator.generate_qr_code(workflow.workflow_id)
    
    assert result['success'] == True
    assert 'qr_id' in result
    
    # Check workflow status
    updated = orchestrator.get_workflow(workflow.workflow_id)
    assert updated['status'] == 'qr_generated'
    
    print("✓ Workflow QR generation test passed")


def test_full_workflow():
    """Test running full workflow."""
    print("Testing full workflow execution...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [
        SignerInfo(signer_id="primary", name="Primary Signer"),
        SignerInfo(signer_id="witness", name="Witness", role=SignerRole.WITNESS)
    ]
    
    result = orchestrator.run_full_workflow(
        document_id="full_test_001",
        title="Complete Test Contract",
        content="Full workflow test content...",
        document_type=DocumentType.CONTRACT,
        created_by="admin",
        signers=signers
    )
    
    assert result['success'] == True
    assert 'workflow_id' in result
    assert result['status'] == 'awaiting_signatures'
    assert 'results' in result
    assert result['results']['steps']['video_render']['success'] == True
    assert result['results']['steps']['signing_start']['success'] == True
    
    print("✓ Full workflow execution test passed")


def test_workflow_cancellation():
    """Test workflow cancellation."""
    print("Testing workflow cancellation...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [SignerInfo(signer_id="signer", name="Signer")]
    workflow = orchestrator.create_workflow(
        document_id="cancel_test",
        title="Cancel Test",
        content="Content",
        document_type=DocumentType.AGREEMENT,
        created_by="admin",
        signers=signers
    )
    
    result = orchestrator.cancel_workflow(
        workflow.workflow_id,
        cancelled_by="admin",
        reason="Testing cancellation"
    )
    
    assert result['success'] == True
    assert result['status'] == 'cancelled'
    
    # Verify status
    updated = orchestrator.get_workflow(workflow.workflow_id)
    assert updated['status'] == 'cancelled'
    
    print("✓ Workflow cancellation test passed")


def test_audit_trail():
    """Test audit trail generation."""
    print("Testing audit trail generation...")
    
    orchestrator = NotaryWorkflowOrchestrator(
        vcode_config={'enable_notifications': False}
    )
    
    signers = [SignerInfo(signer_id="signer", name="Signer")]
    result = orchestrator.run_full_workflow(
        document_id="audit_test",
        title="Audit Test",
        content="Content",
        document_type=DocumentType.CONSENT_FORM,
        created_by="admin",
        signers=signers
    )
    
    workflow_id = result['workflow_id']
    audit_trail = orchestrator.get_audit_trail(workflow_id)
    
    # Should have entries for: creation, video render, qr generation, signing start
    assert len(audit_trail) >= 3
    
    # Check audit entries have required fields
    for entry in audit_trail:
        assert 'timestamp' in entry
        assert 'action' in entry
        assert 'actor_id' in entry
    
    print("✓ Audit trail generation test passed")


def test_signer_roles():
    """Test different signer roles."""
    print("Testing signer roles...")
    
    primary = SignerInfo(
        signer_id="primary",
        name="Primary",
        role=SignerRole.PRIMARY
    )
    assert primary.role == SignerRole.PRIMARY
    
    witness = SignerInfo(
        signer_id="witness",
        name="Witness",
        role=SignerRole.WITNESS
    )
    assert witness.role == SignerRole.WITNESS
    
    notary = SignerInfo(
        signer_id="notary",
        name="Notary",
        role=SignerRole.NOTARY,
        verification_level=VerificationLevel.LEGAL
    )
    assert notary.role == SignerRole.NOTARY
    assert notary.verification_level == VerificationLevel.LEGAL
    
    print("✓ Signer roles test passed")


def run_all_tests():
    """Run all FastDoc tests."""
    print("=" * 80)
    print("Running FastDoc Module Tests")
    print("=" * 80)
    print()
    
    tests = [
        # FFmpeg Adapter Tests
        test_ffmpeg_adapter_initialization,
        test_video_config,
        test_render_job_creation,
        test_contract_video_render,
        
        # QR Generator Tests
        test_qr_generator_initialization,
        test_qr_code_generation,
        test_batch_qr_generation,
        
        # vCODE Integration Tests
        test_vcode_integration_initialization,
        test_signing_request_creation,
        test_signature_capture,
        test_signature_verification,
        
        # Notary Workflow Tests
        test_notary_workflow_orchestrator,
        test_create_notary_workflow,
        test_workflow_video_rendering,
        test_workflow_qr_generation,
        test_full_workflow,
        test_workflow_cancellation,
        test_audit_trail,
        test_signer_roles,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            failed += 1
        print()
    
    print("=" * 80)
    if failed == 0:
        print(f"All {len(tests)} tests passed! ✓")
    else:
        print(f"{failed} of {len(tests)} tests failed ✗")
    print("=" * 80)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
