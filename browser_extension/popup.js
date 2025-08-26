document.addEventListener("DOMContentLoaded", async () => {
  let [tab] = await browser.tabs.query({ active: true, currentWindow: true });

  document.getElementById("title").innerText = tab.title;

  document.getElementById("saveBtn").addEventListener("click", () => {
    const payload = {
      data_path: tab.url,
      metadata_: { title: tab.title }
    };

    browser.runtime.sendMessage({ type: "SAVE_BOOKMARK", payload });
    window.close();
  });
});
