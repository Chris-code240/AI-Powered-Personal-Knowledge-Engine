const API_URL = "https://your-api-domain.com/data";

browser.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type === "SAVE_BOOKMARK") {
    try {
    //   const res = await fetch(API_URL, {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(message.payload)
    //   });

      if (true) {
        console.log(message.payload)
        browser.notifications.create({
          type: "basic",
          iconUrl: browser.runtime.getURL("icons/success.png"),
          title: "Knowledge Engine",
          message: `"${JSON.stringify(message.payload)}" saved successfully!`
        });
      } else {
        throw new Error(`Server responded with ${res.status}`);
      }
    } catch (err) {
      browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/error.png"),
        title: "Knowledge Engine Error",
        message: `Failed to save: ${err.message}`
      });
    }
  }
});
