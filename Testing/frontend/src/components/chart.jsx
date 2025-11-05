import React, { useEffect, useRef, useState, useCallback, useMemo } from 'react';
// Note: Tailwind CSS classes are assumed to be available in the React environment.

// The main component, which contains all logic and rendering for the graph.
const ChartComponent = () => {
    const canvasRef = useRef(null);

    // --- CONFIGURATION START ---

    // Simulated financial data (Y-values). Values scaled for steepness.
    const historicalData = useMemo(() => [
        0,      // START: Explicitly starting at 0 for a baseline
        500, 800, 1500, 
        950, 750, 850, 
        // Exaggerated Drop (Risk) for steepness demonstration
        500, // Significant drop
        1000, 1800, 1600, 1300, 
        // Smaller but still sharp drop
        1100, 
        1400, 1700, 2000, 900, 1700, 3500, 4000, 6000 // Very steep final growth
    ], []);

    // --- Dynamic Speed Calculation for 5-second duration (Faster loop) ---
    const targetDurationSeconds = 15;
    const framesPerSecond = 60;
    const totalFrames = targetDurationSeconds * framesPerSecond; 
    const calculatedSpeed = historicalData.length / totalFrames; 

    // Chart Colors and Aesthetics
    const chartConfig = useMemo(() => ({
        lineColor: '#00F0B0', // Bright Cyan/Green for the main line (Neon effect)
        gridColor: 'rgba(255, 255, 255, 0.05)', // Very faint white for subtle grid
        fillColor: 'rgba(0, 240, 176, 0.1)', // Transparent fill
        dataPointSize: 6,
        animationSpeed: calculatedSpeed,
        glowColor: '#00F0B0',
        glowBlur: 10,
    }), [calculatedSpeed]);

    // Drawing Margins (Reduced padding since labels are removed)
    const padding = 30;
    
    // --- CONFIGURATION END ---

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');        
        let animationFrameId = null; 
        let currentDataIndex = 0;

        // Calculate scaling parameters based on data and canvas size
        const dataMax = Math.max(...historicalData);
        const yMinDisplay = 0; 
        const yMaxDisplay = dataMax * 1.1; 
        const yDisplayRange = yMaxDisplay - yMinDisplay;

        /** Converts a data point's Y value to a canvas Y coordinate. */
        const getYCoordinate = (value) => {
            const chartHeight = canvas.height - 2 * padding;
            const normalized = (value - yMinDisplay) / yDisplayRange;
            return canvas.height - padding - (normalized * chartHeight);
        };

        /** Converts a data point's X index to a canvas X coordinate. */
        const getXCoordinate = (index) => {
            const chartWidth = canvas.width - 2 * padding;
            return padding + (index / (historicalData.length - 1)) * chartWidth;
        };

        /** Draws the static chart elements (grid). */
        const drawStaticElements = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw Y-axis grid lines
            const numLabels = 5;
            for (let i = 0; i < numLabels; i++) {
                const yValue = yMinDisplay + (yDisplayRange / (numLabels - 1)) * i;
                const yCoord = getYCoordinate(yValue);

                // Grid line
                if (i > 0 && i < numLabels - 1) { // Skip top and bottom
                    ctx.strokeStyle = chartConfig.gridColor;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(padding, yCoord);
                    ctx.lineTo(canvas.width - padding, yCoord);
                    ctx.stroke();
                }
            }
        };

        /** The main animation loop. Draws the line incrementally. */
        const animateGraph = () => {
            // Redraw static elements every frame
            drawStaticElements();

            const pointsToDraw = Math.min(Math.ceil(currentDataIndex), historicalData.length);

            if (pointsToDraw > 1) {
                // --- Draw Area Fill ---
                ctx.beginPath();
                ctx.fillStyle = chartConfig.fillColor;
                ctx.moveTo(getXCoordinate(0), canvas.height - padding);
                ctx.lineTo(getXCoordinate(0), getYCoordinate(historicalData[0]));

                // Draw the top boundary of the fill
                for (let i = 0; i < pointsToDraw; i++) {
                    const x = getXCoordinate(i);
                    const y = getYCoordinate(historicalData[i]);
                    ctx.lineTo(x, y);
                }

                // Interpolate the partial segment being drawn
                let finalX = getXCoordinate(pointsToDraw - 1);
                let finalY = getYCoordinate(historicalData[pointsToDraw - 1]);

                if (currentDataIndex < historicalData.length) {
                    const i = pointsToDraw - 1; 
                    const nextI = pointsToDraw; 
                    const fraction = currentDataIndex - i;

                    if (nextI < historicalData.length) {
                        const x1 = getXCoordinate(i);
                        const y1 = getYCoordinate(historicalData[i]);
                        const x2 = getXCoordinate(nextI);
                        const y2 = getYCoordinate(historicalData[nextI]);

                        finalX = x1 + (x2 - x1) * fraction;
                        finalY = y1 + (y2 - y1) * fraction;
                        ctx.lineTo(finalX, finalY);
                    }
                }

                // Complete the fill area
                ctx.lineTo(finalX, canvas.height - padding);
                ctx.closePath();
                ctx.fill();

                // --- Draw Line and Points (with Neon Glow) ---

                ctx.shadowBlur = chartConfig.glowBlur;
                ctx.shadowColor = chartConfig.glowColor;

                ctx.strokeStyle = chartConfig.lineColor;
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(getXCoordinate(0), getYCoordinate(historicalData[0]));

                // Draw the line segments
                for (let i = 1; i < pointsToDraw; i++) {
                    const x = getXCoordinate(i);
                    const y = getYCoordinate(historicalData[i]);
                    ctx.lineTo(x, y);
                }

                // Draw the currently animating segment
                if (currentDataIndex < historicalData.length) {
                    const i = pointsToDraw - 1;
                    const nextI = pointsToDraw;
                    const fraction = currentDataIndex - i;

                    if (nextI < historicalData.length) {
                        const x1 = getXCoordinate(i);
                        const y1 = getYCoordinate(historicalData[i]);
                        const x2 = getXCoordinate(nextI);
                        const y2 = getYCoordinate(historicalData[nextI]);

                        const currentX = x1 + (x2 - x1) * fraction;
                        const currentY = y1 + (y2 - y1) * fraction;

                        ctx.lineTo(currentX, currentY);
                    }
                }
                ctx.stroke();
                ctx.shadowBlur = 0;

                ctx.fillStyle = chartConfig.lineColor;
                for (let i = 0; i < pointsToDraw; i++) {
                        const x = getXCoordinate(i);
                        const y = getYCoordinate(historicalData[i]);
                        ctx.beginPath();
                        ctx.arc(x, y, chartConfig.dataPointSize / 2, 0, Math.PI * 2);
                        ctx.fill();
                }
            }

            // Increment the animation index
            if (currentDataIndex < historicalData.length) {
                currentDataIndex += chartConfig.animationSpeed;
                animationFrameId = requestAnimationFrame(animateGraph);
            } else {
                // *** CONTINUOUS LOOP LOGIC ***
                // Reset index to start the animation over immediately
                currentDataIndex = 0;
                animationFrameId = requestAnimationFrame(animateGraph);
            }
        };


        /** Initializes or restarts the chart animation. */
        const initializeAnimation = () => {
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
            currentDataIndex = 0;
            drawStaticElements();
            animationFrameId = requestAnimationFrame(animateGraph);
        };
        
        // Start the animation on mount
        initializeAnimation();

        // Cleanup function for useEffect: cancels the animation frame
        return () => {
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        };
    }, [historicalData, chartConfig, calculatedSpeed]); 

    return (
        // Container with dark background for the chart itself
        <div className="relative bg-[#0D1117] rounded-xl p-2 border border-gray-700 h-full">
            <canvas 
                ref={canvasRef} 
                id="chartCanvas" 
                width="1100" 
                height="400" 
                className="max-w-full h-auto rounded-xl"
            />
        </div>
    );
};

export default ChartComponent;
