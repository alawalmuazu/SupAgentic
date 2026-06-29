// SupAgentic Optical Override - DOM Injection

console.log("🔮 SupAgentic Optical Override Injected.");

// Construct the Orb DOM Element
const orb = document.createElement("div");
orb.id = "sup-orb";
Object.assign(orb.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    background: "radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.9), rgba(139, 92, 246, 0.8))",
    boxShadow: "0 0 20px rgba(59, 130, 246, 0.5), inset 0 0 10px rgba(255,255,255,0.5)",
    backdropFilter: "blur(10px)",
    cursor: "pointer",
    zIndex: "999999",
    transition: "transform 0.2s ease, box-shadow 0.2s ease",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
});
document.body.appendChild(orb);

// Add hover effects
orb.addEventListener("mouseenter", () => {
    orb.style.transform = "scale(1.1)";
    orb.style.boxShadow = "0 0 30px rgba(59, 130, 246, 0.8), inset 0 0 10px rgba(255,255,255,0.8)";
});
orb.addEventListener("mouseleave", () => {
    orb.style.transform = "scale(1)";
    orb.style.boxShadow = "0 0 20px rgba(59, 130, 246, 0.5), inset 0 0 10px rgba(255,255,255,0.5)";
});

// Notifications
const pushNotification = (text) => {
    const notif = document.createElement("div");
    Object.assign(notif.style, {
        position: "fixed",
        bottom: "75px",
        right: "20px",
        background: "rgba(15, 23, 42, 0.85)",
        color: "#f8fafc",
        padding: "10px 16px",
        borderRadius: "8px",
        backdropFilter: "blur(12px)",
        border: "1px solid rgba(255,255,255,0.1)",
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        fontFamily: "system-ui, sans-serif",
        fontSize: "14px",
        zIndex: "999999",
        opacity: "0",
        transform: "translateY(10px)",
        transition: "all 0.3s ease"
    });
    notif.textContent = text;
    document.body.appendChild(notif);
    
    // Slide in
    setTimeout(() => {
        notif.style.opacity = "1";
        notif.style.transform = "translateY(0)";
    }, 50);
    
    // Fade out
    setTimeout(() => {
        notif.style.opacity = "0";
        setTimeout(() => notif.remove(), 300);
    }, 4000);
};

// WebSocket Telemetry
let ws;
const connectWebSocket = () => {
    ws = new WebSocket("ws://localhost:8789");
    
    ws.onopen = () => {
        orb.style.border = "2px solid rgba(163, 230, 53, 0.5)";
    };
    
    ws.onmessage = (e) => {
        const payload = JSON.parse(e.data);
        if (payload.action === "notify") {
            pushNotification(payload.text);
        }
    };
    
    ws.onclose = () => {
        orb.style.border = "2px solid rgba(244, 63, 94, 0.5)";
        setTimeout(connectWebSocket, 5000); // Reconnect loop
    };
};
connectWebSocket();

// Interactions
orb.addEventListener("click", () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        // Send execution command bridging the DOM into the OS natively
        ws.send(JSON.stringify({
            event: "orb_clicked",
            url: window.location.href,
            title: document.title,
            selection: window.getSelection().toString()
        }));
    } else {
        pushNotification("Error: SupAgentic Bridge Offline");
    }
});
