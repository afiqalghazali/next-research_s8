$(document).ready(function () {
	// DOM Elements
	const videoElement = $("#video")[0];
	const canvasElement = $("#canvas")[0];
	const ctx = canvasElement.getContext("2d");
	const viewModal = $("#view-modal");

	let isCapturing = false; // Flag to track capturing state
	let mediaStream; // Media stream variable

	// Initialize camera access and event listeners
	async function initializeCamera() {
		try {
			mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
			videoElement.srcObject = mediaStream;
			$(document).on("keydown", handleKeyDown);
		} catch (error) {
			alert("Camera access denied. Please check your permissions.");
			console.error("Error accessing camera:", error);
		}
	}

	// Handle keydown events
	function handleKeyDown(event) {
		if (event.code === "Space") {
			event.preventDefault();
			isCapturing ? clearCanvas() : captureImage();
		}
	}

	// Capture image from video stream
	function captureImage() {
		if (isCapturing) return; // Exit if already capturing

		updateCanvasSize();
		ctx.drawImage(
			videoElement,
			0,
			0,
			canvasElement.width,
			canvasElement.height
		);

		toggleVideoCanvasVisibility();
		openModal();
		isCapturing = true; // Set capturing flag
	}

	// Clear the canvas and restart the video
	function clearCanvas() {
		toggleVideoCanvasVisibility();
		isCapturing = false; // Reset capturing flag
	}

	// Helper function to update canvas size
	function updateCanvasSize() {
		canvasElement.width = videoElement.videoWidth;
		canvasElement.height = videoElement.videoHeight;
	}

	// Helper function to toggle visibility of video and canvas
	function toggleVideoCanvasVisibility() {
		$(videoElement).toggleClass("hidden");
		$(canvasElement).toggleClass("hidden");
	}

	// Open the modal
	function openModal() {
		viewModal.removeClass("hidden"); // Show the modal
		$("#overlay").removeClass("hidden"); // Show the overlay
	}

	// Close the modal
	function closeModal() {
		viewModal.addClass("hidden"); // Hide the modal
		$("#overlay").addClass("hidden"); // Hide the overlay
	}

	// Bind the 'View' button to show the captured image in modal
	$("#view-btn").click(function () {
		if (isCapturing) {
			openModal();
		}
	});

	// Bind the close button in modal to close the modal
	$(".close-btn-detail").click(function () {
		closeModal();
	});

	// Start the camera when the document is ready
	initializeCamera();
});
