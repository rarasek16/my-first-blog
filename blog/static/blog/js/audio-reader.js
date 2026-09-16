(() => {
    const readButton = document.querySelector("[data-audio-read]");
    const stopButton = document.querySelector("[data-audio-stop]");
    const status = document.querySelector("[data-audio-status]");
    const main = document.querySelector("main");

    if (!readButton || !stopButton || !status || !main) {
        return;
    }

    if (!("speechSynthesis" in window)) {
        readButton.disabled = true;
        status.textContent = "Hlasové čtení tento prohlížeč nepodporuje.";
        return;
    }

    const stopReading = () => {
        window.speechSynthesis.cancel();
        readButton.setAttribute("aria-pressed", "false");
        stopButton.disabled = true;
    };

    readButton.addEventListener("click", () => {
        stopReading();
        const content = main.cloneNode(true);
        content.querySelector(".audio-controls")?.remove();
        const text = content.innerText.replace(/\s+/g, " ").trim();

        if (!text) {
            status.textContent = "Na této stránce není text k přečtení.";
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "cs-CZ";
        utterance.rate = 1;
        utterance.onend = () => {
            readButton.setAttribute("aria-pressed", "false");
            stopButton.disabled = true;
            status.textContent = "Čtení je dokončeno.";
        };
        utterance.onerror = () => {
            readButton.setAttribute("aria-pressed", "false");
            stopButton.disabled = true;
            status.textContent = "Čtení se nepodařilo spustit.";
        };

        window.speechSynthesis.speak(utterance);
        readButton.setAttribute("aria-pressed", "true");
        stopButton.disabled = false;
        status.textContent = "Probíhá čtení stránky.";
    });

    stopButton.addEventListener("click", () => {
        stopReading();
        status.textContent = "Čtení bylo zastaveno.";
    });

    window.addEventListener("beforeunload", stopReading);
})();
