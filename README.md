# LauzHack Workshop: Python + HTMX

Slides: https://www.canva.com/design/DAF1x9MSMW0/PR8s3_5UASnzGAR2-ZuFKQ/view?utm_content=DAF1x9MSMW0&utm_campaign=designshare&utm_medium=link&utm_source=editor#3

Welcome to the Python + HTMX Workshop! This repository is your comprehensive guide to building scalable web applications using Litestar (a Python backend framework similar to FastAPI), HTMX (HTML Hypertext Markup extension language) and TailwindCSS (to style your app with ease).

You will find two main components in this repository:

- The Python + HTMX tutorial
- Pictorial: a full-featured web application

## 🎓 HTMX Tutorial

This tutorial houses three basic examples that would guide you to understand and implement HTMX in your web applications effectively.

- **Live Data Update**: Showcases how to fetch real-time stock data from the backend every second and append rows in a table.
- **Form Submission**: Demonstrates submitting a form containing an image URL and a size, and getting the image resized without reloading the page. Plus, there's an automatic change trigger to query the backend for a size preview and image preview.
- **Filtering & Sorting**: Here you'll encounter a form with fake client data, filter text and a select option. You'll learn how to make the form submit changes and replace the body when either of the inputs change.

### 🧑🏽‍💻 Getting Started

1. Clone the repository
2. Install poetry
3. Run `poetry install`
4. Enter the env shell: `poetry shell`
5. Run `doit -n 2 dev_tutorial`

## 🚀 Pictorial: Full-Featured Application

Pictorial is a sophisticated web application that combines Python with HTMX in a realistic scenario. It allows people to singup, login, and generate images in parallel (up to 3 prompts) using OpenAI DALLE-3. Users can also visit their library containing all their image generations.

Key Features:

- Effortless User Registration: Offers streamlined signup capabilities, enabling new users to create accounts and access customized functionalities quickly.
- Secure Authentication: Includes robust login/logout functionality with secure password handling, ensuring a secure and personalized user experience.
- Interactive Content Creation: Utilizes OpenAI API for on-the-fly image generation based on user prompts, providing an engaging and interactive platform.
- Personalized Libraries: Allows users to save and revisit their generated images in a personal library that's dynamically updated using htmx.

The Pictorial Web Application exemplifies a modern approach to web development, merging backend and frontend technologies to create a responsive and interactive platform without relying on complex JavaScript frameworks.

### 🧑🏽‍💻 Getting started

1. Clone the repository
2. Install poetry
3. Install Dbmate
4. Run `poetry install`
5. Enter the env shell: `poetry shell`
6. Create a `.env`
7. Add to the `.env`: `DATABASE_URL=sqlite:db/db.sqlite3`
8. Add to the `.env`: `OPENAI_API_KEY=<YOUR_API_KEY>`
9. Run `doit -n 2 db_reset`
10. Run `doit -n 2 dev`
