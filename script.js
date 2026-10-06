console.log("StyleAI script loaded");


const form = document.querySelector(".style-form");


// =====================================================
// FORM SUBMIT
// =====================================================

form.addEventListener("submit", async function (event) {

    // STOP NORMAL HTML FORM RELOAD
    event.preventDefault();


    const occasion =
        document.getElementById("occasion").value;

    const height =
        document.getElementById("height").value;

    const style =
        document.getElementById("style").value;

    const color =
        document.getElementById("color").value;

    const season =
        document.getElementById("season").value;


    // =================================================
    // VALIDATION
    // =================================================

    if (
        !occasion ||
        !height ||
        !style ||
        !color ||
        !season
    ) {

        alert(
            "Please fill in all fields."
        );

        return;
    }


    // =================================================
    // FORM DATA
    // =================================================

    const formData = new FormData();

    formData.append(
        "occasion",
        occasion
    );

    formData.append(
        "height",
        height
    );

    formData.append(
        "style",
        style
    );

    formData.append(
        "color",
        color
    );

    formData.append(
        "season",
        season
    );


    // =================================================
    // BUTTON
    // =================================================

    const button =
        form.querySelector(
            ".generate-button"
        );

    const originalText =
        button.innerHTML;


    button.disabled = true;

    button.innerHTML =
        "✨ Generating your outfit...";


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/recommend",
                {
                    method: "POST",

                    body: formData,

                    credentials: "include"
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.error ||
                "Something went wrong."
            );

            return;
        }


        showRecommendation(result);


    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to the Python server. " +
            "Please make sure app.py is running."
        );


    } finally {

        button.disabled = false;

        button.innerHTML =
            originalText;

    }

});


// =====================================================
// SHOW RESULT
// =====================================================

function showRecommendation(result) {

    const oldResult =
        document.getElementById(
            "recommendation-result"
        );


    if (oldResult) {

        oldResult.remove();

    }


    const resultBox =
        document.createElement("div");


    resultBox.id =
        "recommendation-result";


    resultBox.innerHTML = `

        <div class="outfit-result">

            <div class="result-badge">
                ✨ AI RECOMMENDATION
            </div>

            <h2>
                ${result.outfit.title}
            </h2>

            <p class="result-description">
                Your StyleAI recommendation
                is based on your selected
                occasion, style, color,
                weather and garment proportion.
            </p>


            <div class="result-grid">

                <div class="result-item">

                    <span>Occasion</span>

                    <strong>
                        ${result.occasion}
                    </strong>

                </div>


                <div class="result-item">

                    <span>Preferred Style</span>

                    <strong>
                        ${result.style}
                    </strong>

                </div>


                <div class="result-item">

                    <span>Height</span>

                    <strong>
                        ${result.height} cm
                    </strong>

                </div>


                <div class="result-item">

                    <span>Favorite Color</span>

                    <strong>
                        ${result.color}
                    </strong>

                </div>

            </div>


            <div class="outfit-details">

                <div>

                    <span>👕 Top</span>

                    <p>
                        ${result.outfit.top}
                    </p>

                </div>


                <div>

                    <span>👖 Bottom</span>

                    <p>
                        ${result.outfit.bottom}
                    </p>

                </div>


                <div>

                    <span>👟 Shoes</span>

                    <p>
                        ${result.outfit.shoes}
                    </p>

                </div>


                <div>

                    <span>⌚ Accessories</span>

                    <p>
                        ${result.outfit.accessories}
                    </p>

                </div>

            </div>


            <div class="style-notes">

                <p>
                    🎨 ${result.outfit.color_note}
                </p>

                <p>
                    🌦️ ${result.outfit.weather_note}
                </p>

                <p>
                    📏 ${result.outfit.height_note}
                </p>

            </div>


            <div class="dataset-status">

                ${
                    result.dataset.loaded
                    ? `AI embedding database loaded:
                       ${result.dataset.items} items`
                    : `AI embedding database not found`
                }

            </div>

        </div>
    `;


    form.parentElement.appendChild(
        resultBox
    );


    resultBox.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// =====================================================
// LOGIN
// =====================================================

async function loginUser(
    email,
    password
) {

    const response =
        await fetch(
            "http://127.0.0.1:5000/login",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                credentials: "include",

                body: JSON.stringify({
                    email,
                    password
                })
            }
        );


    return await response.json();

}


// =====================================================
// SIGN UP
// =====================================================

async function signupUser(
    name,
    email,
    password
) {

    const response =
        await fetch(
            "http://127.0.0.1:5000/signup",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                credentials: "include",

                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            }
        );


    return await response.json();

}
