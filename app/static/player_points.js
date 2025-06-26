// player_points.js: tally player points based on selected checkboxes and grade points
window.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.player-checkbox');
    const totalPointsSpan = document.getElementById('total-points');
    function tallyPoints() {
        let total = 0;
        checkboxes.forEach(cb => {
            if (cb.checked) {
                const points = parseInt(cb.getAttribute('data-points'), 10) || 0;
                total += points;
            }
        });
        totalPointsSpan.textContent = total;
    }
    checkboxes.forEach(cb => cb.addEventListener('change', tallyPoints));
});
