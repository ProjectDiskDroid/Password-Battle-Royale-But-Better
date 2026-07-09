
// =============================================================================
// ANIMATED BACKGROUND
// =============================================================================

let pageCleanup = null;

function launchPageEffect(container) {
    const bgLayer = document.createElement('div');
    bgLayer.className = 'animated-bg';
    container.insertBefore(bgLayer, container.firstChild);

    const create = createStarTunnel;
    if (!create) return null;

    const destroy = create(bgLayer);
    return () => {
        destroy();
        bgLayer.remove();
    };
}

/** Start a persistent animated background on the given element (e.g. document.body). */
export function startPageBackground(container) {
    stopPageBackground();
    pageCleanup = launchPageEffect(container);
}

/** Stop and remove the page-level background. */
export function stopPageBackground() {
    if (pageCleanup) {
        pageCleanup();
        pageCleanup = null;
    }
}

// Updates the speed of the star tunnel
let speed = 8;

export function setBgStarSpeed(newSpeed) {
    speed = newSpeed;
}

// =============================================================================
// STAR TUNNEL
// =============================================================================
// Perspective-projected stars stream outward from the center with fading trails.

function createStarTunnel(container) {
    const canvas = document.createElement('canvas');
    Object.assign(canvas.style, { width: '100%', height: '100%', display: 'block' });
    container.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let W = container.clientWidth || 300;
    let H = container.clientHeight || 600;
    canvas.width = W;
    canvas.height = H;

    const STAR_COUNT = 450;
    const COLORS = [
        [76,   29,  149],  // dark purple
        [124,  58,  237],  // mid purple
        [168,  85,  247],  // light purple
        [216,  180, 254],  // pale purple
    ];

    const stars = Array.from({ length: STAR_COUNT }, () => ({
        x:  (Math.random() - 0.5) * W * 2,
        y:  (Math.random() - 0.5) * H * 2,
        z:  Math.random() * W,
        pz: 0,
        ci: Math.floor(Math.random() * COLORS.length),
    }));

    // Original: ctx.fillStyle = '#1a1917'; ctx.fillRect(0, 0, W, H);
    // Changed to clearRect so the canvas is transparent (no black background).
    ctx.clearRect(0, 0, W, H);

    let running = true;
    let raf;
    // const speed = 10;

    const tick = () => {
        if (!running) return;

        // Trail effect without a background color:
        // 'destination-out' fades existing canvas pixels by reducing their alpha each frame.
        // Lower alpha = slower fade = longer trails. Raise it to shorten trails.
        // (Original approach used a dark fillRect which baked in a black background.)
        ctx.globalCompositeOperation = 'destination-out';
        ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
        ctx.fillRect(0, 0, W, H);
        ctx.globalCompositeOperation = 'source-over';

        const cx = W / 2;
        const cy = H / 2;

        for (const s of stars) {
            s.pz = s.z;
            s.z -= speed;

            if (s.z <= 0.5) {
                s.x  = (Math.random() - 0.5) * W * 2;
                s.y  = (Math.random() - 0.5) * H * 2;
                s.z  = W;
                s.pz = W;
                continue;
            }

            const sx = (s.x / s.z)  * (W * 0.25) + cx;
            const sy = (s.y / s.z)  * (H * 0.25) + cy;
            const px = (s.x / s.pz) * (W * 0.25) + cx;
            const py = (s.y / s.pz) * (H * 0.25) + cy;

            const depth = 1 - s.z / W;
            const size  = Math.max(0.3, depth * 2.5);
            const alpha = depth * 0.75;
            const c = COLORS[s.ci];

            ctx.strokeStyle = `rgba(${c[0]},${c[1]},${c[2]},${alpha * 0.6})`;
            ctx.lineWidth = size * 0.8;
            ctx.beginPath();
            ctx.moveTo(px, py);
            ctx.lineTo(sx, sy);
            ctx.stroke();

            ctx.fillStyle = `rgba(${c[0]},${c[1]},${c[2]},${alpha})`;
            ctx.beginPath();
            ctx.arc(sx, sy, size * 0.6, 0, Math.PI * 2);
            ctx.fill();
        }

        raf = requestAnimationFrame(tick);
    };

    raf = requestAnimationFrame(tick);

    return () => {
        running = false;
        cancelAnimationFrame(raf);
        canvas.remove();
    };
}

