# Chai & Chakkar

**Play Live:** https://saiqulmodi.github.io/chai-and-chakkar/

A zero-install HTML5 Canvas physics merge game where players drop and combine 14 tiers of treats inside a brass dabba container, featuring periodic Chakkar gravity tilts, Level 1 to Infinity progression, and real-time 2-player WebSocket duels.

## Features
- **14-Tier Merge Progression:** Merge from Elaichi, Rasgulla, Kulfi Stick, and Samosa up to Masala Dosa and the Royal Veg Thali (+50,000 Grand Feast blast).
- **4 Switchable 14-Item Packs + Custom Builder:** Switch between 14 Veg Food & Drinks, Fruits & Smoothies, Sweets & Ice Creams, Cafe & Bakery, or build a custom 14-item pack inside Menu -> 14 Items.
- **Infinite Level 1 to Infinity & Daily Seed Mode:** Advance through endless levels or play deterministic daily runs.
- **On-Demand Drop Hint:** Unlocks at 500 points for 5 guided drops and recharges every +1,000 points.
- **2-Player Room Links:** Instant same-browser sync plus cross-device WebSocket duels via server.py.
- **Shareable Score Cards:** Downloadable PNG score cards for sharing high scores.

## Local Multiplayer Relay Setup
    pip install fastapi uvicorn websockets
    python server.py
    tailscale funnel --bg --set-path=/ws http://127.0.0.1:8765/ws

