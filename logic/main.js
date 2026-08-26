/**
 * Auto Do - Main Application Logic, UI Handlers & Toast System
 */

// Global Toast System
window.showToast = function(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  let icon = '🔔';
  if (type === 'success') icon = '✨';
  if (type === 'info') icon = 'ℹ️';
  if (type === 'warning') icon = '⚠️';

  toast.innerHTML = `
    <span>${icon}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s, transform 0.3s';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
};

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileNav = document.getElementById('mobile-nav');

  if (mobileMenuBtn && mobileNav) {
    mobileMenuBtn.addEventListener('click', () => {
      const isHidden = mobileNav.classList.contains('hidden');
      if (isHidden) {
        mobileNav.classList.remove('hidden');
        mobileNav.classList.add('flex');
      } else {
        mobileNav.classList.add('hidden');
        mobileNav.classList.remove('flex');
      }
    });
  }

  // Window Dots simulation
  const dotRed = document.querySelector('.dot-red');
  const dotYellow = document.querySelector('.dot-yellow');
  const dotGreen = document.querySelector('.dot-green');
  const appShell = document.querySelector('.autodo-app-shell');

  if (dotRed && appShell) {
    dotRed.addEventListener('click', () => {
      appShell.style.transition = 'all 0.3s ease';
      appShell.style.transform = 'scale(0.8)';
      appShell.style.opacity = '0.3';
      window.showToast('App window minimized.', 'info');
      setTimeout(() => {
        appShell.style.transform = 'scale(1)';
        appShell.style.opacity = '1';
      }, 1200);
    });
  }

  if (dotYellow && appShell) {
    dotYellow.addEventListener('click', () => {
      window.showToast('App collapsed to tray.', 'info');
    });
  }

  if (dotGreen && appShell) {
    dotGreen.addEventListener('click', () => {
      window.showToast('Maximized mode toggled.', 'info');
    });
  }

  // Download Action Handler
  const downloadBtns = document.querySelectorAll('.btn-download');
  downloadBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.showToast('🚀 Downloading DENM Auto-Do v2.4.0 (Windows x64)...', 'success');
      
      // Simulate download trigger after short timeout
      setTimeout(() => {
        const dummyLink = document.createElement('a');
        dummyLink.setAttribute('href', '#');
        dummyLink.setAttribute('download', 'AutoDo_Setup_v2.4.0.exe');
        window.showToast('✅ Download initiated! Check your downloads folder.', 'success');
      }, 1000);
    });
  });

  // Launch App Action Handler
  const launchBtns = document.querySelectorAll('.btn-launch-app');
  launchBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      window.showToast('🚀 Opening Auto Do Desktop Application...', 'success');
    });
  });

  // Copy code / shortcuts snippet handler
  const copyBtns = document.querySelectorAll('.btn-copy');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetText = btn.getAttribute('data-copy') || btn.textContent.trim();
      navigator.clipboard.writeText(targetText).then(() => {
        window.showToast(`📋 Copied "${targetText}" to clipboard!`, 'success');
      }).catch(() => {
        window.showToast('📋 Copied to clipboard!', 'success');
      });
    });
  });
});
