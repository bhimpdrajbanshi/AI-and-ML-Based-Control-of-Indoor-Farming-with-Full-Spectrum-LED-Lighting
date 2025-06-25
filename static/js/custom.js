// static/js/form-utils.js

function validateRequiredFields(formSelector) {
  let isValid = true;

  // Loop through required fields
  $(`${formSelector} [required]`).each(function () {
    const value = $(this).val().trim();

    if (!value) {
      const fieldName = $(this).attr('name') || 'This field';
      toastr.error(`${fieldName} is required`);
      $(this).focus();
      isValid = false;
      return false; // exit .each early
    }
  });

  return isValid;
}


// static/js/form-utils.js

function handleAjaxError(xhr) {
  try {
    const json = JSON.parse(xhr.responseText);
    const msg = Array.isArray(json.error)
      ? json.error.join('<br>')
      : json.error;

    toastr.error(msg || "Unexpected error occurred.");
  } catch (e) {
    toastr.error("Unexpected error occurred.");
  }
}


function validatePhoneNumber(inputId, maxLength = 10) {
  $('#' + inputId).on('input', function () {
    // Remove all non-digit characters
    this.value = this.value.replace(/\D/g, '');

    // Trim to maxLength digits if longer
    if (this.value.length > maxLength) {
      this.value = this.value.slice(0, maxLength);
    }
  });

}