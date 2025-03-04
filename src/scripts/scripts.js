// Registration Form Script
$(document).ready(function () {
	// Configuration
	const CONFIG = {
		units: [
			"Prodi Ilmu Komputer",
			"Prodi Matematika",
			"Prodi Pendidikan Matematika",
			"Prodi Matematika Bilingual",
		],
		orientations: [
			"Hadap depan",
			"Hadap kiri",
			"Hadap kanan",
			"Hadap bawah",
			"Hadap atas",
		],
	};

	// DOM Elements
	const $elements = {
		videoPreview: $("#videoPreview")[0],
		captureCanvas: $("#captureCanvas")[0],
		capturedImagesContainer: $("#capturedImagesContainer"),
		registrationForm: $("#registrationForm"),
		orientationInstruction: $("#orientationInstruction"),
		nextStepButtons: $(".next-step"),
		prevStepButtons: $(".prev-step"),
	};

	// Initialize Unit Dropdown
	function initializeUnitDropdown() {
		const $unitSelect = $("#unit");
		CONFIG.units.forEach((unit) => {
			$unitSelect.append(`<option value="${unit}">${unit}</option>`);
		});

		$(".select2-fields").select2({
			placeholder: "Masukkan Unit Kerja/Prodi",
			allowClear: true,
			minimumResultsForSearch: 0,
		});
	}

	// Image Capture Module
	const ImageCaptureModule = {
		capturedImages: [],

		capturePhoto() {
			if (this.capturedImages.length >= 5) return;

			const context = $elements.captureCanvas.getContext("2d");
			$elements.captureCanvas.width = $elements.videoPreview.videoWidth;
			$elements.captureCanvas.height = $elements.videoPreview.videoHeight;

			context.drawImage(
				$elements.videoPreview,
				0,
				0,
				$elements.captureCanvas.width,
				$elements.captureCanvas.height
			);

			const imageDataUrl = $elements.captureCanvas.toDataURL("image/jpeg");
			const orientation = CONFIG.orientations[this.capturedImages.length];

			this.capturedImages.push({
				dataUrl: imageDataUrl,
				orientation: orientation,
			});

			this.updateDisplay();
			this.updateInstructions();
			this.checkCaptureCompletion();
		},

		deleteAllPhoto() {
			this.capturedImages = [];
			this.updateDisplay();
			this.updateInstructions();
			this.checkCaptureCompletion();
			this.startInitialInstruction();
		},

		updateDisplay() {
			$elements.capturedImagesContainer.empty();
			this.capturedImages.forEach((image) => {
				const $imageWrapper = $(`
                    <div class="flex flex-col items-center bg-blue-600 rounded-lg size-40 m-2 p-1">
                        <img src="${image.dataUrl}" class="h-full object-cover rounded-t-lg">
                        <div class="flex text-xs text-white font-semibold justify-center items-center p-2 rounded-b-lg">
                            ${image.orientation}
                        </div>
                    </div>
                `);
				$elements.capturedImagesContainer.append($imageWrapper);
			});
		},

		updateInstructions() {
			const nextIndex = this.capturedImages.length;
			if (nextIndex < CONFIG.orientations.length) {
				$elements.orientationInstruction.html(
					`Posisi: <span class="font-bold">${CONFIG.orientations[nextIndex]}</span>. Tekan SPACEBAR untuk mengambil foto`
				);
			} else {
				$elements.orientationInstruction.text("Semua foto telah diambil");
			}
		},

		startInitialInstruction() {
			// Set initial instruction to first orientation
			$elements.orientationInstruction.html(
				`Posisi: <span class="font-bold">${CONFIG.orientations[0]}</span>. Tekan SPACEBAR untuk mengambil foto`
			);
		},

		checkCaptureCompletion() {
			const isComplete = this.capturedImages.length === 5;
			$(".next-step[data-next-step='3']").prop("disabled", !isComplete);

			if (isComplete) {
				this.updateConfirmationImages();
			}
		},

		updateConfirmationImages() {
			const $confirmContainer = $("#confirmationImagesContainer");
			$confirmContainer.empty();

			this.capturedImages.forEach((image) => {
				const $imageWrapper = $(`
                    <div class="flex flex-col items-center bg-blue-600 rounded-lg size-40 m-2 p-1">
                        <img src="${image.dataUrl}" class="h-full object-cover rounded-t-lg">
                        <div class="flex text-xs text-white font-semibold justify-center items-center p-2 rounded-b-lg">
                            ${image.orientation}
                        </div>
                    </div>
                `);
				$confirmContainer.append($imageWrapper);
			});
		},

		async startCamera() {
			try {
				$(document).off("keydown");
				const stream = await navigator.mediaDevices.getUserMedia({
					video: true,
				});
				$elements.videoPreview.srcObject = stream;

				this.startInitialInstruction();

				$(document).on("keydown", (e) => {
					if (e.code === "Space") {
						e.preventDefault();
						this.capturePhoto();
					}
				});
			} catch (err) {
				alert("Camera access denied. Please check your permissions.");
				console.error("Error accessing camera:", err);
			}
		},
	};

	// Step Navigation Module
	const StepNavigationModule = {
		navigateStep(currentStep, direction) {
			const totalSteps = 3;

			// Hide all steps and show current step
			$(".registration-step").addClass("hidden");
			$(`#step${currentStep}`).removeClass("hidden");

			// Update progress bar
			const progress = ((currentStep - 1) / (totalSteps - 1)) * 100;
			$("#progressBar").css("width", `${progress}%`);

			// Update step indicators
			this.updateStepIndicators(currentStep, totalSteps);

			// Special step handling
			this.handleSpecificSteps(currentStep, direction);
		},

		updateStepIndicators(currentStep, totalSteps) {
			for (let i = 1; i <= totalSteps; i++) {
				const $indicator = $(`#step${i}Indicator`);
				$indicator.removeClass(
					"bg-blue-600 bg-gray-300 text-white text-gray-600"
				);

				if (i < currentStep) {
					$indicator.addClass("bg-blue-600 text-white");
				} else if (i === currentStep) {
					$indicator.addClass("bg-blue-600 text-white");
				} else {
					$indicator.addClass("bg-gray-300 text-gray-600");
				}
			}
		},

		handleSpecificSteps(currentStep, direction) {
			if (currentStep === 2) {
				ImageCaptureModule.startCamera();
			} else if (currentStep !== 2) {
				const stream = $elements.videoPreview.srcObject;
				if (stream) {
					const tracks = stream.getTracks();
					tracks.forEach((track) => track.stop());
					$elements.videoPreview.srcObject = null;
				}
			}

			if (currentStep === 3) {
				this.updateConfirmationDetails();
			}
		},

		updateConfirmationDetails() {
			$("#confirmName").text($("#fullname").val());
			$("#confirmIdentityNumber").text($("#identityNumber").val());
			$("#confirmUnit").text($("#unit").val());
		},
	};

	// Form Validation Module
	const FormValidationModule = {
		initValidation() {
			// Disable next buttons initially
			$elements.nextStepButtons.prop("disabled", true);

			// Validate first step
			$("#registrationForm input, #registrationForm select").on(
				"change input",
				function () {
					const allFieldsFilled = $(
						"#registrationForm input, #registrationForm select"
					)
						.toArray()
						.every((el) => $(el).val() !== "");

					$(".next-step[data-next-step='2']").prop(
						"disabled",
						!allFieldsFilled
					);
				}
			);
		},
	};

	// Event Bindings
	function bindEvents() {
		// Next Step Handlers
		$elements.nextStepButtons.click(function () {
			const nextStep = $(this).data("next-step");
			StepNavigationModule.navigateStep(nextStep, "next");
		});

		// Previous Step Handlers
		$elements.prevStepButtons.click(function () {
			const prevStep = $(this).data("prev-step");
			StepNavigationModule.navigateStep(prevStep, "prev");
		});

		// Delete Pictures Button Handler
		$("#deletePicturesBtn").click(function () {
			ImageCaptureModule.deleteAllPhoto();
		});

		// Form Submission
		$elements.registrationForm.submit(function (e) {
			e.preventDefault();
			alert("Registration Submitted Successfully!");
			// Implement actual submission logic here
		});
	}

	// Initialization
	function init() {
		initializeUnitDropdown();
		FormValidationModule.initValidation();
		bindEvents();
	}

	// Start the application
	init();
});
