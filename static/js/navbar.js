$(document).ready(function () {
	$('[data-drawer-toggle="logo-sidebar"]').on("click", function () {
		$("#logo-sidebar").toggleClass("-translate-x-full");
	});
	$(document).on("click", function (e) {
		const $dropdown = $("#user-dropdown");
		const $button = $("#user-menu-button");

		// If clicking on the button
		if ($(e.target).closest("#user-menu-button").length) {
			$dropdown.toggleClass("hidden");
			$button.attr(
				"aria-expanded",
				$button.attr("aria-expanded") === "true" ? "false" : "true"
			);
			return false;
		}

		// Close dropdown if clicking outside
		if (!$(e.target).closest("#user-dropdown").length) {
			$dropdown.addClass("hidden");
			$button.attr("aria-expanded", "false");
		}
	});
});
