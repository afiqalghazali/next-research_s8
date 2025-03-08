$(document).ready(function () {
	// Function to open the delete modal
	function openDeleteModal(button) {
		var userName = button.data("user-name");
		var deleteUrl = button.attr("href");
		$("#delete-modal-description").html(
			"Apakah kamu yakin untuk menghapus<br><strong>" + userName + "</strong>?"
		);
		$("#delete-btn").attr(
			"onclick",
			'window.location.href="' + deleteUrl + '"'
		);
		$("#delete-modal, #overlay").removeClass("hidden");
	}

	// Function to close the modal
	function closeModal(modal) {
		modal.addClass("hidden");
		$("#overlay").addClass("hidden");
	}

	// Function to show user details in the modal
	function showUserDetails(button) {
		var userId = button.data("user-id");
		var userIdentity = button.data("user-identity");
		var userName = button.data("user-name");
		var userUnit = button.data("user-unit");

		$("#identityNumber").text(userIdentity);
		$("#name").text(userName);
		$("#unit").text(userUnit);
		$("#imagesContainer").empty();

		fetchUserImages(userId);
		$("#detail-modal, #overlay").removeClass("hidden");
	}

	// Function to fetch images for the user
	function fetchUserImages(userId) {
		var orientations = ["depan", "kiri", "kanan", "bawah", "atas"];
		$.ajax({
			url: "/user/" + userId + "/images",
			method: "GET",
			success: function (data) {
				data.forEach(function (imgObj, index) {
					var orientation = orientations[index % orientations.length];
					var imageDiv = `  
						<div class="flex flex-col items-center bg-blue-600 rounded-lg size-40 m-2 p-1">  
							<img title="User Image" src="data:image/jpeg;base64,${imgObj.base64}" class="w-full object-cover rounded-t-lg h-5/6" />  
							<div class="w-full flex items-center h-1/6 text-xs sm:text-sm text-white font-semibold p-2 justify-center rounded-b-lg">  
								Hadap ${orientation}  
							</div>  
						</div>`;
					$("#imagesContainer").append(imageDiv);
				});
			},
			error: function (err) {
				console.error("Failed to load images", err);
			},
		});
	}

	// Event listeners
	$(".delete-btn").on("click", function (e) {
		e.preventDefault();
		openDeleteModal($(this));
	});

	$(".no-btn").on("click", function () {
		closeModal($("#delete-modal"));
	});

	$(".detail-btn").on("click", function () {
		showUserDetails($(this));
	});

	$(".close-btn-detail").on("click", function () {
		closeModal($("#detail-modal"));
	});
});
