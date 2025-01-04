
# **Hand-Tracked Pong Game**  

This project is a modern twist on the classic **Pong** game, using **hand tracking** via a **camera**. It leverages **Mediapipe** for real-time hand tracking and **Pygame** for graphics and game logic.  

---

## **1. Video Demonstration**  

A demonstration video is available here: [Demo Video](https://ecambxl-my.sharepoint.com/:v:/g/personal/20342_ecam_be/EWN56YcbRVdOoesArpRXUNABSeCi_wzm4YNCh-Kc-lmoww?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=aX5J2q)  

![Capture d'écran 2025-01-04 160451](https://github.com/user-attachments/assets/644f7907-0db8-4e39-ad9a-fe3a6e7450bf)
---

## **2. Features**  

- **Hand-controlled paddles**:  
  Uses **Mediapipe** to detect finger positions and move paddles.  
- **Automatic start**:  
  The game begins when both hands are detected and index brought close together.  
- **Progressive speed**:  
  The ball speeds up after each bounce to increase difficulty.  
- **Real-time scoring**:  
  Scores update dynamically after each round.  

---

## **3. Installation and Requirements**  

### **Dependencies**  

Install Python 3.x and the following libraries:  

```bash
pip install opencv-python mediapipe pygame numpy
```

---

## **4. How It Works**  

### **Initialization**  
1. Start the camera feed using **OpenCV**.  
2. Enable hand tracking with **Mediapipe**.  
3. Create the game interface using **Pygame**.  

### **Hand Tracking Controls**  
4. Detect **index finger tips** to control paddle movements vertically.  
5. Change paddle color: **red** when no hand is detected, **green** when detected.  

### **Game Logic**  
6. The ball moves and bounces off walls and paddles, gaining speed after each bounce.  
7. Scores are updated when a player scores a point.  

---

## **5. Known Limitations**  

- **Performance issues**:  
  - Frequent **lag** caused by intensive hand recognition processing.  
  - Noticeable **slowdowns** when multiple computations are performed in real time.  

- **Ball physics issues**:  
  - Some **bugs** in collision handling at **paddle corners**.  

- **Boost version abandoned**:  
  An experimental version added a **boost** feature where bringing the **thumb and index finger close together** reduced the paddle size and increased ball speed. However, this version caused excessive **lag** and became **unplayable**, so it was **abandoned**.  

---

## **6. Future Improvements**  

- **Performance optimization**:  
  Reduce CPU load from hand-tracking computations.  
- **Collision fixes**:  
  Resolve errors in ball rebounds at paddle corners.  
- **Improved fluidity**:  
  Implement predictive algorithms to handle hand detection dropouts.  
- **Enhanced visuals and sound effects**:  
  Add animations and sounds to make the game more engaging.  

---


## **7. Dependencies**  

### Python Libraries:  
- **OpenCV** (`cv2`) - Camera management and video processing.  
- **Mediapipe** - Machine-learning-based hand tracking.  
- **Pygame** - Graphics and game engine.  
- **Numpy** - Mathematical calculations for ball physics.  
- **Random** - Random generation of ball directions.  

---

## **8. Usage**  

1. Run the game with:  
   ```bash
   python pong_game.py
   ```

2. Position your hands in front of the camera to control the paddles.  
3. The game starts automatically when both hands are detected and brought close together.  

---

## **9. Contributions**  

Contributions are welcome to:  
- Optimize performance.  
- Fix bugs.  
- Add new features and gameplay modes.  

---
