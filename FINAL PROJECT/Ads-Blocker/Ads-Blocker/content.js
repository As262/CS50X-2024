// Function to remove video ads on YouTube
function removeYouTubeAds() {
    const adSelectors = [
      ".video-ads",           // General video ads container
      ".ytp-ad-module",       // YouTube player ad module
      ".ytp-ad-overlay-slot", // Overlay ads in YouTube videos
    ];

    adSelectors.forEach((selector) => {
      const ads = document.querySelectorAll(selector);
      ads.forEach((ad) => ad.remove());
    });

    // Skip ad button, if present
    const skipButton = document.querySelector(".ytp-ad-skip-button");
    if (skipButton) {
      skipButton.click();
    }
  }

  // Run the ad removal function periodically
  setInterval(removeYouTubeAds, 1000);
