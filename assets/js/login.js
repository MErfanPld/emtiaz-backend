// Password visibility toggle
    let isPasswordVisible = false;
    function togglePasswordVisibility() {
      const passwordInput = document.getElementById('password');
      const eyeIcon = document.getElementById('eye-icon');
      const eyeSlashIcon = document.getElementById('eye-slash-icon');
      
      isPasswordVisible = !isPasswordVisible;
      if (isPasswordVisible) {
        passwordInput.type = 'text';
        eyeIcon.classList.add('hidden');
        eyeSlashIcon.classList.remove('hidden');
      } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('hidden');
        eyeSlashIcon.classList.add('hidden');
      }
    }

    // Interactive Demo Handlers
    function triggerDefaultState() {
      const usernameInput = document.getElementById('username');
      const passwordInput = document.getElementById('password');
      const usernameError = document.getElementById('username-error');
      const passwordError = document.getElementById('password-error');
      const credAlert = document.getElementById('credentials-alert');
      const submitBtn = document.getElementById('submit-btn');
      const submitText = document.getElementById('submit-btn-text');
      const submitSpinner = document.getElementById('submit-spinner');

      usernameInput.classList.remove('field-error');
      passwordInput.classList.remove('field-error');
      usernameError.classList.add('hidden');
      passwordError.classList.add('hidden');
      credAlert.classList.add('hidden');

      submitBtn.disabled = false;
      submitText.textContent = 'ورود به پنل مدیریت';
      submitSpinner.classList.add('hidden');
    }

    function triggerValidationError() {
      triggerDefaultState();
      const usernameInput = document.getElementById('username');
      const passwordInput = document.getElementById('password');
      const usernameError = document.getElementById('username-error');
      const passwordError = document.getElementById('password-error');

      usernameInput.value = '';
      passwordInput.value = '';

      usernameInput.classList.add('field-error');
      passwordInput.classList.add('field-error');
      usernameError.classList.remove('hidden');
      passwordError.classList.remove('hidden');
    }

    function triggerInvalidCredentials() {
      triggerDefaultState();
      const usernameInput = document.getElementById('username');
      const passwordInput = document.getElementById('password');
      const credAlert = document.getElementById('credentials-alert');

      usernameInput.value = 'admin@emtiaz.ir';
      passwordInput.value = '••••••••';
      usernameInput.classList.add('field-error');
      passwordInput.classList.add('field-error');
      credAlert.classList.remove('hidden');
    }

    function triggerLoadingState() {
      triggerDefaultState();
      const submitBtn = document.getElementById('submit-btn');
      const submitText = document.getElementById('submit-btn-text');
      const submitSpinner = document.getElementById('submit-spinner');

      submitBtn.disabled = true;
      submitText.textContent = 'در حال ورود...';
      submitSpinner.classList.remove('hidden');

      setTimeout(() => {
        triggerDefaultState();
      }, 3500);
    }

    function handleSubmit() {
      const usernameInput = document.getElementById('username');
      const passwordInput = document.getElementById('password');

      if (!usernameInput.value.trim() || !passwordInput.value.trim()) {
        triggerValidationError();
      } else {
        triggerLoadingState();
      }
    }
