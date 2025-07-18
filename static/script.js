// // Show/Hide Diagnosis Options
//  document.getElementById('getDiagnosisBtn').addEventListener('click', function() {
//      const options = document.getElementById('diagnosisOptions');
//     options.style.display = options.style.display === 'block' ? 'none' : 'block';
//  });

// Upload Image
// document.getElementById('uploadBtn').addEventListener('click', function() {
//          document.getElementById('imageUpload').click();
//  });

// document.getElementById('imageUpload').addEventListener('change', function(event) {
//     const imagePreview = document.getElementById('imagePreview');
//     imagePreview.src = URL.createObjectURL(event.target.files[0]);
//     imagePreview.style.display = 'block';
//     document.getElementById('camera').style.display = 'none';
//     document.getElementById('capturePhotoBtn').style.display = 'none';
// });

// Capture Image from Camera
document.getElementById('captureBtn').addEventListener('click', function() {
    const camera = document.getElementById('camera');
    const capturePhotoBtn = document.getElementById('capturePhotoBtn');
    camera.style.display = 'block';
    capturePhotoBtn.style.display = 'inline-block';
    document.getElementById('imagePreview').style.display = 'none';
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            camera.srcObject = stream;
            camera.play();
        });
    }
});

document.getElementById('capturePhotoBtn').addEventListener('click', function() {
    const camera = document.getElementById('camera');
    const imagePreview = document.getElementById('imagePreview');
    const canvas = document.createElement('canvas');
    canvas.width = camera.videoWidth;
    canvas.height = camera.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(camera, 0, 0, canvas.width, canvas.height);
    imagePreview.src = canvas.toDataURL('image/png');
    imagePreview.style.display = 'block';
    camera.style.display = 'none';
    document.getElementById('capturePhotoBtn').style.display = 'none';
    // Stop the camera stream
    const stream = camera.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
