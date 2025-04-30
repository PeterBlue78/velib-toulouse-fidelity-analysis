# Velib Toulouse Fidelity Analysis

## Context

As a regular user of the "Vélo Toulouse" bike-sharing service for over a year, I became increasingly curious about the fidelity point system. Users can earn 10 fidelity points by returning a bike to a designated "bonus" station, which in turn allows them to reserve a bike for 15 minutes. However, I noticed that I rarely received points, and the official documentation or website provided no clear explanation about how or when points were awarded.

This project was born out of a personal need to better understand and optimize the earning of fidelity points. Since no reliable resource was available online, I decided to build my own dataset and analyze the patterns myself.

---

## Tools & Technologies

To carry out this analysis, I used the following tools:

- **DBeaver**: to perform SQL-based data analysis and queries
- **Python**: to collect real-time data from the JCDecaux API (used by Vélo Toulouse)
- **JCDecaux API**: I registered and created my own API key on their official platform

The goal was to automate data collection and perform exploratory analysis to detect favorable times, locations, or station types where fidelity points are more likely to be awarded.

---

## Project Structure

