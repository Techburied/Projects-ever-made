let timer;
var workMinutes = 50;
let breakMinutes = 10;
let seconds = 0;
let isWorkSession = true;
let isTimerRunning = false;
let isPaused = false;

function startYouTubePlayer() {
    player = new YT.Player('youtubePlayer', {
        height: '360',
        width: '640',
        videoId: 'jfKfPfyJRdk',
        
    });
}

window.onload = function () {
    startYouTubePlayer();
};

function resetTimer() {
    clearInterval(timer);
    isTimerRunning = false;
    workMinutes = 50;
    breakMinutes = 10;
    seconds = 0;
    isWorkSession = true;
    updateDisplay();
}

function updateTimer() {
    if (workMinutes === 0 && seconds === 0 && isWorkSession) {
        clearInterval(timer);
        isTimerRunning = false;
        alert("Work session completed! Take a break.");
        workMinutes = 50; // Reset work session time to 2 minutes
        seconds = 0;
        isWorkSession = false;
        updateDisplay();
        setTimeout(() => {
            startBreak();
        }, 1000);
    } else if (breakMinutes === 0 && seconds === 0 && !isWorkSession) {
        clearInterval(timer);
        isTimerRunning = false;
        alert("Break session completed! Back to work.");
        breakMinutes = 10; // Reset break time to 1 minute
        seconds = 0;
        isWorkSession = true;
        updateDisplay();
        setTimeout(() => {
            startTimer();
        }, 1000);
    } else {
        if (seconds === 0) {
            if (isWorkSession) {
                workMinutes--;
            } else {
                breakMinutes--;
            }
            seconds = 59;
        } else {
            seconds--;
        }
    }
    updateDisplay();
}

function startBreak() {
    alert("Break time! Take a break.");
    isWorkSession = false;
    startTimer();
}

function updateDisplay() {
    const displayMinutes = isWorkSession ? workMinutes : breakMinutes;
    const displaySeconds = seconds < 10 ? `0${seconds}` : seconds;
    const timerDisplay = document.getElementById("timer");
    timerDisplay.innerText = `${displayMinutes}:${displaySeconds}`;
}

function startTimer() {
    clearInterval(timer);
    isTimerRunning = false;
    isPaused = false;

    // Only start a new timer if it's not already running
    if (!isTimerRunning) {
        timer = setInterval(updateTimer, 1000);
        isTimerRunning = true;
    }
}


function pauseTimer() {
    clearInterval(timer);
    isTimerRunning = false;
    isPaused = true;
}

function resumeTimer() {
    startTimer();
    isPaused = false;
}

document.getElementById("pauseResumeButton").addEventListener("click", function () {
    if (isTimerRunning || isPaused) {
        if (isPaused) {
            resumeTimer();
        } else {
            pauseTimer();
        }
        updateDisplay();
    }
});
function toggleVideo() {
    if (player.getPlayerState() === 1) {  // 1 represents playing state
        player.pauseVideo();
    } else if (player.getPlayerState() === 2) {  // 2 represents paused state
        player.playVideo();
    }
}
