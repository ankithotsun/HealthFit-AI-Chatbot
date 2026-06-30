"""
HealthFit AI Chatbot — Intent Dataset Generator

This script compiles a balanced dataset of 34 intents, with exactly 75 patterns per intent
(totaling 2,550 high-quality patterns) and 10 response templates per intent.
"""

import json
import os
import random

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "intents.json"
)

# Core prefixes for pattern expansion
PREFIXES = [
    "",
    "tell me ",
    "what is ",
    "how to ",
    "i want ",
    "suggest ",
    "give me ",
    "guide on ",
    "explain ",
    "help with "
]

BLUEPRINTS = [
    {
        "tag": "greeting",
        "bases": [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy", "whats up",
            "greetings", "hi there", "hello there", "how are you", "how's it going", "how have you been",
            "nice to meet you", "yo", "namaste", "satsriakal", "hola", "hey chatbot", "hello assistant",
            "helo", "hy", "goodevening", "goodmorning", "good nite", "heyllo"
        ],
        "responses": [
            "Hello! I am HealthFit AI, your personal health and fitness assistant. How can I help you today?",
            "Hi there! Welcome to HealthFit AI. Ask me anything about workouts, diet, BMI, or wellness!",
            "Hey! Great to see you. I am here to help with all your health and fitness questions.",
            "Good day! How can I assist you with your fitness and health goals today?",
            "Greetings! Ready to work on your fitness? Ask me anything!",
            "Hello! Stay active and ask me about nutrition, workouts, or calculation tools.",
            "Hi! Let's get moving today. What health tips are you looking for?",
            "Hey there! Health is wealth. Ask me about stretching, cardio, or calorie needs.",
            "Hello there! I am excited to help you on your wellness journey today.",
            "Hi! Welcome back. What can I do for your workout or diet routine today?"
        ]
    },
    {
        "tag": "goodbye",
        "bases": [
            "bye", "goodbye", "see you", "see you later", "take care", "farewell", "exit", "quit",
            "finished", "bye bye", "gotta go", "i am leaving", "talk to you later", "have a good day",
            "good night", "catch you later", "alvida", "chalo bye", "phir milenge", "byebye", "tata"
        ],
        "responses": [
            "Goodbye! Stay active and take care of your health. Come back anytime!",
            "See you later! Remember, consistency is the key to a healthy lifestyle.",
            "Take care! Keep moving, stay hydrated, and get enough sleep. Goodbye!",
            "Farewell! Keep working towards your wellness goals.",
            "Goodbye! Make healthy choices today. See you soon!",
            "Bye! Don't forget to track your water and nutrition today.",
            "Catch you later! Keep active and stay positive.",
            "Have a wonderful day! Keep up the good work on your fitness journey.",
            "Goodbye! I'll be here whenever you need more fitness or health tips.",
            "Goodbye! Remember that small daily efforts lead to big results."
        ]
    },
    {
        "tag": "thanks",
        "bases": [
            "thank you", "thanks", "thanks a lot", "thank you so much", "helpful", "perfect",
            "awesome", "appreciate it", "great help", "many thanks", "thank u", "shukriya", "dhanyawad",
            "thankyou", "thx", "tanks", "very helpful", "super helpful", "you are the best", "great chatbot"
        ],
        "responses": [
            "You are most welcome! Feel free to ask if you have more health or fitness questions.",
            "Happy to help! Your health matters. Let me know if there is anything else I can assist with.",
            "Glad I could be of help! Stay consistent with your fitness goals and you will see great results.",
            "My pleasure! Let's keep working towards a healthier lifestyle.",
            "Anytime! I am glad you found the information useful.",
            "You're welcome! Keep learning and staying active.",
            "Glad to help. Feel free to ask about exercises, meal plans, or BMR targets.",
            "You got it! Stay focused on your health journey.",
            "Happy to assist you today! Don't hesitate to reach out if you have more queries.",
            "Awesome! Let me know if you need any other assistance."
        ]
    },
    {
        "tag": "bot_identity",
        "bases": [
            "who are you", "your name", "about yourself", "what are you", "explain how you work",
            "introduce yourself", "who made you", "developer info", "system designer", "who created you",
            "app details", "what is this app", "kon ho aap", "apka naam kya hai", "kisne banaya", "bot name"
        ],
        "responses": [
            "I am HealthFit AI, an intelligent chatbot designed to provide general health and fitness guidance using NLP and Machine Learning.",
            "I am your HealthFit AI Assistant. I use natural language processing to help you analyze your fitness goals.",
            "My name is HealthFit AI. I was created as a project to guide users in nutrition, calculations, and training.",
            "I am a traditional NLP chatbot built with Flask and scikit-learn, specializing in health and fitness queries.",
            "I am HealthFit AI! I help users estimate BMI, calculate calorie needs, and find suitable workouts.",
            "I am an automated health assistant designed to make fitness advice accessible and easy to understand.",
            "I work by classifying your messages into fitness categories and extracting key entities like weight and goals.",
            "I am your virtual personal trainer and dietitian, powered by a traditional hybrid NLP classification model.",
            "I am HealthFit AI. I assist with exercise selection, hydration targets, and healthy eating guides.",
            "I am a virtual wellness companion created to showcase how machine learning can support healthy lifestyles."
        ]
    },
    {
        "tag": "help",
        "bases": [
            "help", "what can i ask", "how to use this", "options", "guide me", "topics covered",
            "features", "help guide", "instructions", "list commands", "madad", "help please", "what do you do"
        ],
        "responses": [
            "I cover a wide range of topics: workouts (HIIT, weight loss, muscle gain), diets (keto, vegan, vegetarian), specific exercises (squats, pushups), nutritional advice, BMI calculation, and stress/sleep management.",
            "You can ask me questions like: 'How to calculate BMI?', 'What is a good protein source?', or 'Give me a leg workout.'",
            "I can assist you with exercise instructions, daily hydration targets, and calculating your estimated BMR.",
            "Need help? You can check your BMI by entering your weight and height, or ask for beginner exercise suggestions.",
            "I am equipped to suggest meal plans (breakfast, lunch, dinner) and help you configure calorie budgets.",
            "You can type things like: 'keto diet tips', 'how much water to drink', or 'strength training guides.'",
            "To use session memory, just tell me your weight or goal, and ask questions later like 'how much protein should I eat?'",
            "I am ready to help you with sleep requirements, stress reduction tips, and stretching guides.",
            "Ask me about workouts (legs, core, upper body) or food highlights like eggs, chicken, and oats.",
            "I can guide you on general health queries. Just type your question or ask for topic suggestions!"
        ]
    },
    {
        "tag": "bmi",
        "bases": [
            "calculate bmi", "what is bmi", "bmi formula", "am i overweight", "am i underweight",
            "body mass index", "check my weight", "find bmi", "bmi check", "weigth height index",
            "bmi kaise nikalte hai", "bmi kya hai", "mota hu ya patla", "cal bmi", "bmiscore"
        ],
        "responses": [
            "BMI (Body Mass Index) evaluates weight relative to height using: BMI = Weight (kg) / Height (m)^2. {bmi_calc}\n\nCategories:\n• Below 18.5: Underweight\n• 18.5-24.9: Normal\n• 25-29.9: Overweight\n• 30+: Obese.",
            "Your Body Mass Index (BMI) indicates whether you are in a healthy weight range. {bmi_calc}",
            "To check if your weight is proportional to your height, we calculate BMI. {bmi_calc}",
            "BMI helps assess body weight categories. The formula is Weight in kg divided by Height in meters squared. {bmi_calc}",
            "Let's check your BMI category (Underweight, Normal, Overweight, or Obese). {bmi_calc}",
            "A high BMI can indicate high body fatness, while a low BMI indicates low mass. {bmi_calc}",
            "Evaluating your Body Mass Index (BMI) is a great step to understand your baseline health. {bmi_calc}",
            "Using your physical parameters, we calculate your BMI score and assign a standard category. {bmi_calc}",
            "BMI calculations are general indicators. Consult a physician for an in-depth analysis. {bmi_calc}",
            "Knowing your BMI helps tailor your nutrition and workout intensity. Let's find it. {bmi_calc}"
        ]
    },
    {
        "tag": "calorie_estimation",
        "bases": [
            "calculate calories", "calorie needs", "how many calories", "calorie estimator",
            "daily calorie intake", "burn calories", "calorie requirement", "tdee check", "bmr calculation",
            "calories budget", "calories daily", "calorie count", "calorie check", "calories kitna chahiye"
        ],
        "responses": [
            "Your daily calorie needs depend on your age, weight, gender, activity level, and goal (weight loss or muscle gain). {calorie_advice}",
            "Let's estimate your daily Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE). {calorie_advice}",
            "To weight lose or gain muscle, you must manage your daily calorie budget. {calorie_advice}",
            "We calculate your maintenance calories and recommend targets for your goals. {calorie_advice}",
            "Managing calorie intake is the foundation of energy balance. Here is your estimate. {calorie_advice}",
            "Based on your profile metrics, we can estimate how many calories your body burns daily. {calorie_advice}",
            "Here is the estimated calorie allocation to support weight loss or muscle building. {calorie_advice}",
            "Whether you want to create a deficit or a surplus, here are your calculated calorie limits. {calorie_advice}",
            "Understanding your calorie expenditure helps optimize fat loss or muscle hypertrophy. {calorie_advice}",
            "Calculate your custom calorie metrics to align your meal portions and macros. {calorie_advice}"
        ]
    },
    {
        "tag": "hydration",
        "bases": [
            "water intake", "how much water", "hydration rule", "dehydration", "drink daily",
            "water requirements", "pani kitna pina chahiye", "water target", "how much water to drink",
            "dehydration prevention", "water daily", "fluid intake", "pani kitna piye", "hydration goals"
        ],
        "responses": [
            "A general rule of thumb is to drink 3-4 liters of water daily for active individuals. {hydration_advice}",
            "Hydration is critical for cellular function, energy levels, and joint health. {hydration_advice}",
            "Make sure to drink water consistently throughout the day to avoid dehydration. {hydration_advice}",
            "Let's calculate a custom hydration goal based on your physical weight. {hydration_advice}",
            "Drinking enough fluids supports digestion, nutrient absorption, and skin health. {hydration_advice}",
            "Your body is mostly water. Keep it replenished to support performance and metabolism. {hydration_advice}",
            "Aim to consume water before, during, and after your training sessions. {hydration_advice}",
            "Dehydration can cause fatigue, headaches, and drop physical performance. {hydration_advice}",
            "Here is your personalized daily water consumption guideline. {hydration_advice}",
            "Drink plenty of water. Adjust this upward if you exercise in warm climates. {hydration_advice}"
        ]
    },
    {
        "tag": "sleep",
        "bases": [
            "sleep needs", "insomnia", "tired", "sleep hours", "rest and recovery", "sleep quality",
            "sleeping requirements", "how much sleep", "nind kitni chahiye", "sleep benefit",
            "good sleep", "lack of sleep", "sleeping cycles", "rest recovery", "insomnia help"
        ],
        "responses": [
            "Getting 7-9 hours of quality sleep daily is crucial for muscle recovery and hormonal balance. {sleep_advice}",
            "Sleep is when your body repairs muscle tissue and consolidates memory. Prioritize it. {sleep_advice}",
            "A lack of sleep can increase cortisol levels and hinder fat loss or muscle gain. {sleep_advice}",
            "To maximize athletic recovery, focus on both sleep duration and deep sleep quality. {sleep_advice}",
            "Aim for a consistent sleep schedule by going to bed and waking up at the same time. {sleep_advice}",
            "Avoid screens and caffeine close to bedtime to improve your sleep latency. {sleep_advice}",
            "Your age determines your recommended sleep range. Let's see your targets. {sleep_advice}",
            "Rest and recovery are just as important as your training session. Sleep well. {sleep_advice}",
            "Quality sleep improves cognitive function, immunity, and athletic output. {sleep_advice}",
            "Here is your personalized sleep guidance based on your profile details. {sleep_advice}"
        ]
    },
    {
        "tag": "workout_beginner",
        "bases": [
            "beginner workout", "start exercising", "workout for newbies", "first time exercising",
            "easy exercises", "gym kab jana chahiye", "exercise kab karni chahiye", "starting gym",
            "beginner routine", "simple exercises", "gym basics", "how to exercise first time",
            "shuruat kaise kare exercise ki", "newbie training", "workout basics"
        ],
        "responses": [
            "For beginners, a simple full-body routine 3 times a week is best. Focus on squats, pushups, walking, and light stretching.",
            "Starting out? Focus on learning correct form before adding heavy weights.",
            "Beginner programs should prioritize consistency and mobility over extreme intensity.",
            "An ideal starter routine involves basic movements like bodyweight squats, lunges, and brisk walking.",
            "Aim for 2 to 3 sessions per week with at least 48 hours of rest between workouts.",
            "Do not rush the process. Start with 20-30 minutes of light activity and build up slowly.",
            "As a beginner, compound movements are your best tool to build general strength.",
            "Ensure you warm up dynamically for 5 minutes before initiating any routine.",
            "A balanced beginner routine targets all major muscle groups twice a week.",
            "Start your fitness journey with sustainable habits, simple structures, and safe movements."
        ]
    },
    {
        "tag": "workout_weight_loss",
        "bases": [
            "weight loss workout", "exercises to lose weight", "fat burning routine", "burn fat exercises",
            "shed fat workout", "weight kaise kam kare", "pet ki charbi kaise kam kare", "mujhe patla hona hai",
            "fat loss workout", "hiit workout", "burn calories exercises", "cardio for fat loss",
            "lose weight gym", "fat loss exercises", "patla hone ka workout", "hiit cardio"
        ],
        "responses": [
            "To support your weight loss goal, combine cardio (running or HIIT) with resistance training. {weight_loss_exercise_advice}",
            "Fat loss is achieved when you combine regular calorie burning with a moderate diet deficit. {weight_loss_exercise_advice}",
            "High-Intensity Interval Training (HIIT) is highly efficient for burning calories in short periods. {weight_loss_exercise_advice}",
            "Cardio sessions like running, cycling, or swimming are great to increase your energy output. {weight_loss_exercise_advice}",
            "Do not neglect lifting weights; building muscle keeps your metabolic rate high during fat loss. {weight_loss_exercise_advice}",
            "Combine compound lifts (squats, deadlifts) with active recovery for optimal body composition. {weight_loss_exercise_advice}",
            "A structured weight loss program includes 3 lifting sessions and 2 cardio sessions weekly. {weight_loss_exercise_advice}",
            "HIIT alternates high-intensity work with rest periods to boost your metabolic rate. {weight_loss_exercise_advice}",
            "Consistency is crucial. Find activities you enjoy, whether it's running, rowing, or swimming. {weight_loss_exercise_advice}",
            "Shedding fat requires patience and a structured workout plan. Let's get active! {weight_loss_exercise_advice}"
        ]
    },
    {
        "tag": "workout_muscle_gain",
        "bases": [
            "muscle gain workout", "exercises to build muscle", "strength training routine",
            "hypertrophy workout", "bulk up exercises", "muscle kaise banaye", "build muscle",
            "muscle growth exercises", "body building routine", "progressive overload workout",
            "gain size exercises", "muscle banani hai", "bulkup exercises", "hypertrophy training"
        ],
        "responses": [
            "To support your muscle gain goal, focus on progressive overload with compound lifts (squats, deadlifts, bench press). {muscle_gain_exercise_advice}",
            "Muscle hypertrophy requires lifting weights with sufficient volume and intensity close to failure. {muscle_gain_exercise_advice}",
            "Aim to train each major muscle group 2 times per week for optimal synthesis. {muscle_gain_exercise_advice}",
            "Include compound exercises like overhead presses, pullups, and squats in your workouts. {muscle_gain_exercise_advice}",
            "Ensure you are eating enough protein and resting sufficiently to allow your fibers to repair. {muscle_gain_exercise_advice}",
            "Track your weights and reps to guarantee you are progressively overloading your muscles. {muscle_gain_exercise_advice}",
            "To build size, target a rep range of 6-12 repetitions per set with high intensity. {muscle_gain_exercise_advice}",
            "Combine a slight caloric surplus with structured lifting to build clean muscle mass. {muscle_gain_exercise_advice}",
            "Consistency in the gym and progressive resistance training are key to muscle gain. {muscle_gain_exercise_advice}",
            "Focus on structural compound lifts to recruit maximum muscle fibers and spark growth. {muscle_gain_exercise_advice}"
        ]
    },
    {
        "tag": "healthy_breakfast",
        "bases": [
            "healthy breakfast", "breakfast ideas", "what to eat in morning", "morning meal suggestions",
            "healthy morning food", "oats breakfast", "protein breakfast", "nashte me kya khaye",
            "subah ka khana", "breakfast options", "best breakfast list", "nashta suggestions"
        ],
        "responses": [
            "A healthy breakfast should contain complex carbs and proteins. Good options include oatmeal with chia seeds, egg omelets, or a protein smoothie.",
            "Start your day with high-quality protein and fiber to maintain stable blood sugar levels.",
            "Eggs with whole-grain toast or Greek yogurt with berries are quick, healthy morning options.",
            "Fuel your morning with complex carbohydrates like rolled oats or quinoa bowls.",
            "A good breakfast helps set your satiety levels and provides energy for early workouts.",
            "Try a meal with avocado, egg whites, and spinach for a nutrient-dense breakfast.",
            "Avoid sugary pastries or cereals in the morning, which cause energy crashes.",
            "Oatmeal topped with walnuts, almonds, and sliced banana is a great fuel source.",
            "For a quick option, blend protein powder, spinach, banana, and almond milk.",
            "Your morning meal should align with your daily macro targets. Choose clean foods."
        ]
    },
    {
        "tag": "healthy_lunch",
        "bases": [
            "healthy lunch", "lunch ideas", "midday meal", "what to eat for lunch",
            "lunch options", "fitness lunch", "balanced lunch", "dopahar ka khana",
            "lunch macro meal", "diet lunch ideas", "quick lunch recipes", "lunch suggestions"
        ],
        "responses": [
            "A balanced lunch includes lean protein, fiber-rich veggies, and complex carbs. Example: Grilled chicken salad with quinoa and avocado.",
            "Keep your energy levels high with a lunch of turkey wraps, mixed greens, and olive oil dressing.",
            "Tofu stir-fry with broccoli, carrots, and brown rice is a great vegetarian lunch choice.",
            "Prepare a clean lunch containing salmon, sweet potatoes, and steamed green beans.",
            "A healthy lunch prevents the afternoon slump and supports muscle recovery.",
            "For a light meal, try cottage cheese, mixed greens salad, and a handful of almonds.",
            "Incorporate variety by mixing lentils, chickpeas, and colored bell peppers in a salad bowl.",
            "For a high-protein option, prepare chicken breast with quinoa and avocado.",
            "Opt for whole grains instead of refined carbs to stay full and active all afternoon.",
            "Combine lean beef or beans with roasted broccoli and a portion of white or brown rice."
        ]
    },
    {
        "tag": "healthy_dinner",
        "bases": [
            "healthy dinner", "dinner ideas", "night meal", "what to eat for dinner",
            "dinner options", "light dinner", "dinner recipes", "raat ka khana",
            "night dinner list", "diet dinner ideas", "dinner macro meal", "dinner suggestions"
        ],
        "responses": [
            "For dinner, a lighter option is ideal. Try baked salmon with broccoli and sweet potatoes, or a tofu stir-fry with brown rice.",
            "A dinner with lean beef, asparagus, and roasted sweet potatoes is highly nutrient-dense.",
            "Avoid heavy, high-fat meals right before sleep to prevent digestive issues.",
            "Chicken breast alongside steamed spinach and quinoa makes a perfect recovery dinner.",
            "Grilled paneer or tempeh with roasted mixed vegetables is a clean dinner choice.",
            "Opt for high-protein, high-fiber, and moderate-carb dinners to support muscle repair overnight.",
            "A healthy dinner aids in overnight muscle recovery and regulates morning hunger.",
            "Try white fish like cod or tilapia with a large green salad and olive oil.",
            "Lentil soup with a side of mixed vegetables is a warming, healthy dinner option.",
            "Balance your dinner plate with 1/3 protein, 1/3 green vegetables, and 1/3 complex carbs."
        ]
    },
    {
        "tag": "dietary_patterns",
        "bases": [
            "keto diet", "ketogenic lifestyle", "low carb high fat", "ketosis guidelines", "keto food list",
            "vegan diet", "plant based eating", "vegan protein sources", "no animal products", "vegan nutrition",
            "vegetarian meal", "vegetarian food list", "no meat diet", "vegetarian protein", "veggie based meal plan",
            "intermittent fasting", "fasting window", "16 8 fast", "time restricted eating", "how to fast"
        ],
        "responses": [
            "Different dietary patterns include Keto, Vegan, Vegetarian, and Intermittent Fasting. {keto_advice} {vegan_advice}",
            "A ketogenic diet focuses on fat adaptation, while vegan and vegetarian diets focus on plant-based nutrition.",
            "Intermittent fasting restricts eating windows (e.g., 16 hours fasting) rather than changing what food you consume.",
            "Choose a dietary pattern that is sustainable for your lifestyle and supports your wellness goals.",
            "Ensure that whatever diet you follow provides adequate micronutrients, minerals, and vitamins.",
            "Keto restricts carbs severely, whereas plant-based diets rely on clean carbs like beans and quinoa.",
            "Intermittent fasting can assist with caloric control by limiting the hours you consume food.",
            "For vegan diets, supplement with vitamin B12 and monitor protein intake using beans and tofu.",
            "Vegetarians can leverage dairy, eggs, paneer, and whey protein to hit daily macro goals easily.",
            "Consult a clinical dietitian before starting extreme calorie restrictions or elimination diets."
        ]
    },
    {
        "tag": "healthy_snacks",
        "bases": [
            "healthy snacks", "snacks for weight loss", "low calorie snacks", "fitness snacks", "high protein snacks",
            "fruits to eat", "healthy fruits", "benefits of fruits", "best fruit list",
            "vegetables to eat", "healthy veggies", "benefits of veggies", "best green vegetables",
            "fruits vegetables benefits", "snacks ideas", "what to eat when hungry"
        ],
        "responses": [
            "Great healthy snacks include mixed nuts, Greek yogurt with berries, rice cakes with peanut butter, apple slices, or boiled eggs.",
            "Snacking on fresh fruits (apples, bananas, berries) provides essential fiber, vitamins, and fast energy.",
            "Vegetables like carrots, cucumbers, and cherry tomatoes are low-calorie and high-volume, keeping you full.",
            "For a high-protein snack, try beef jerky, hard-boiled eggs, or cottage cheese.",
            "Choose whole-food snacks over processed chips or sweets to prevent energy fluctuations.",
            "Hummus with cucumber slices or celery sticks makes a refreshing, fiber-rich snack.",
            "A handful of almonds or walnuts provides healthy fats and sustains satiety between meals.",
            "Eating fruits and veggies daily supports digestion and delivers essential antioxidants.",
            "Protein bars and whey shakes are convenient snacks to meet macros when busy.",
            "Limit high-sugar snacks; opt for complex carbs, clean fats, and lean protein options instead."
        ]
    },
    {
        "tag": "protein_sources",
        "bases": [
            "protein sources", "what has protein", "best protein foods", "lean protein list",
            "protein kitna lena chahiye", "whey protein", "protein powder supplements", "how to take whey",
            "whey shake", "protein intake", "daily protein requirement", "protein foods list",
            "bodybuilding protein", "veg protein sources"
        ],
        "responses": [
            "Excellent protein sources include eggs, chicken breast, fish (salmon/tuna), Greek yogurt, cottage cheese, tofu, lentils, and whey protein. {whey_advice}",
            "Aim to consume 1.6 to 2.2 grams of protein per kilogram of body weight to support muscle recovery.",
            "Whey protein is a fast-absorbing dairy supplement that makes meeting daily protein requirements easy and safe.",
            "Eggs and chicken breast are classic, bioavailable protein sources for building lean mass.",
            "Plant-based protein includes tofu, tempeh, lentils, chickpeas, and vegan protein powders.",
            "Ensure you distribute your protein intake evenly across 3-5 meals throughout the day.",
            "Lifting weights creates micro-tears in muscle fibers; protein provides amino acids to repair them.",
            "Fish like salmon and tuna provide high-quality protein along with healthy fatty acids.",
            "Greek yogurt and cottage cheese are excellent slow-digesting protein options before bed.",
            "Hinglish speakers ask: protein kitna lena chahiye? Aim for a portion of protein in every major meal."
        ]
    },
    {
        "tag": "motivation",
        "bases": [
            "workout motivation", "stay consistent", "feel lazy", "discipline in fitness",
            "fitness journey mindset", "no motivation", "lazy gym", "mental strength",
            "consistency tips", "motivation quotes", "how to build discipline", "fitness goals focus"
        ],
        "responses": [
            "Consistency beats intensity. Set small, daily targets and remember why you started. Focus on showing up every single day!",
            "Motivation gets you started; discipline is what keeps you going when you feel lazy.",
            "Do not wait for the perfect feeling. Action creates motivation. Put on your gym shoes and start moving.",
            "Focus on the process, not just the end result. Celebrate small daily victories in your habits.",
            "Your health is an investment, not an expense. Be patient with your progress.",
            "Write down your fitness goals and review them daily to stay focused and aligned.",
            "Find a workout partner or community to keep you accountable on your fitness journey.",
            "Track your workouts and weights; seeing your numerical progress is highly motivating.",
            "Remember that a bad workout is still better than no workout at all. Show up!",
            "Be kind to yourself on off days, but remain committed to your long-term wellness vision."
        ]
    },
    {
        "tag": "stress_management",
        "bases": [
            "stress relief", "cortisol levels", "reduce anxiety", "mental health fitness", "relax mind",
            "how to manage stress", "meditation benefits", "anxiety relief exercises", "stress reduction",
            "relaxing tips", "cortisol management", "mental recovery", "anxious feel"
        ],
        "responses": [
            "Chronic stress raises cortisol which impairs recovery. Practice deep breathing, meditation, yoga, and ensure you get sufficient sleep.",
            "Manage stress by taking regular breaks, spending time in nature, and disconnecting from screens.",
            "Deep breathing exercises for 5 minutes can instantly lower your heart rate and acute anxiety.",
            "Physical exercise is a powerful outlet to release endorphins and combat mental fatigue.",
            "Ensure a healthy work-life balance to prevent burnout and keep your recovery optimal.",
            "Meditation and mindfulness practices help reduce activity in the brain's emotional center.",
            "Avoid overtraining, which is a physical stressor that raises baseline cortisol levels.",
            "Prioritize laughing, hobbies, and social connections to maintain cognitive and emotional health.",
            "A relaxed mind sleeps better, recovers faster, and performs stronger in the gym.",
            "If stress feels unmanageable, consider consulting a mental health professional for tailored advice."
        ]
    },
    {
        "tag": "yoga_stretching",
        "bases": [
            "yoga exercises", "yoga poses", "asana practice", "benefits of yoga", "yoga for flexibility",
            "stretching routines", "flexibility training", "stretches for soreness", "warm up stretching",
            "cool down stretches", "flexibility poses", "improve flexibility", "mobility training",
            "tight muscles", "joint range of motion", "stretching guide"
        ],
        "responses": [
            "Yoga and static stretching improve flexibility, core strength, joint mobility, and reduce stress.",
            "Perform dynamic stretching before a workout to warm up, and static stretches after to cool down.",
            "Focus on essential yoga poses like Downward Dog, Cobra Pose, and Child's Pose for recovery.",
            "Holding stretches for 20-30 seconds helps elongate tight muscles and increases range of motion.",
            "Daily mobility routines protect your joints from injury and improve lifting mechanics.",
            "Yoga connects movement with deep breathing, helping relax both your mind and nervous system.",
            "Stretching sore muscles promotes blood flow, which accelerates nutrient delivery and recovery.",
            "Do not force a stretch to the point of pain; focus on mild discomfort and breathe deeply.",
            "Yoga is excellent for core stabilization, balance, and general body awareness.",
            "Incorporate a 10-minute stretching session post-workout to maintain muscle elasticity."
        ]
    },
    {
        "tag": "cardio_workout",
        "bases": [
            "cardio workout", "running jogging", "cardiovascular exercises", "aerobic workouts",
            "treadmill routine", "improve stamina", "build endurance", "stamina exercises",
            "how to run longer", "cardio capacity", "swimming cycling", "stamina gain"
        ],
        "responses": [
            "Cardio is vital for cardiovascular health, lung capacity, and calorie expenditure. {cardio_advice}",
            "Build stamina by starting with brisk walking, then jogging, and slowly increasing your duration.",
            "Try Zone 2 cardio (aerobic pacing where you can hold a conversation) for endurance base building.",
            "Incorporate activities like running, cycling, swimming, rowing, or skipping into your routine.",
            "Aim for 150 minutes of moderate cardiovascular activity weekly to maintain optimal heart health.",
            "Cardio training strengthens your heart muscle, lowering your resting heart rate over time.",
            "Interval training (cardio sprints) alternates high intensity and rest to build peak conditioning.",
            "Consistency in cardio builds lung capacity and improves recovery time between weight sets.",
            "Ensure you wear supportive footwear to protect your joints during high-impact running.",
            "Vary your cardio machines (treadmill, elliptical, rower) to prevent repetitive stress injuries."
        ]
    },
    {
        "tag": "strength_training",
        "bases": [
            "strength training", "weight lifting", "resistance training", "building strength",
            "compound movements", "deadlifts form", "deadlift safety", "how to deadlift",
            "back deadlift", "barbell deadlift", "bench press", "chest press form",
            "barbell bench press", "how to bench press", "bench press safety", "upper body workout",
            "chest back shoulders arms", "strength upper body"
        ],
        "responses": [
            "Strength training improves bone density, builds lean muscle, and boosts metabolic rate.",
            "Focus on core compound movements like the bench press, deadlift, squats, and overhead press.",
            "Aim for 3 to 4 strength training sessions weekly, allowing 48 hours for muscle recovery.",
            "Progressive overload—gradually increasing weight or reps—is the foundation of building strength.",
            "The bench press targets chest and triceps; keep your feet flat and retract your shoulders.",
            "Deadlifts engage your entire posterior chain. Keep your spine neutral and drive with your legs.",
            "Always warm up with light sets before attempting heavier resistance training weights.",
            "Lifting weights supports fat loss by preserving metabolically active muscle tissue.",
            "Focus on perfect lifting form to prevent injuries and maximize target muscle recruitment.",
            "Record your strength metrics weekly to verify you are making progressive overload gains."
        ]
    },
    {
        "tag": "body_weight_exercises",
        "bases": [
            "pushups form", "how to do pushups", "proper push up", "chest pushups",
            "pullups form", "how to do pullups", "chin ups guide", "pull up exercises",
            "lats training", "plank exercise", "core plank", "how to hold plank",
            "plank time", "ab planks", "calisthenics", "bodyweight training"
        ],
        "responses": [
            "Bodyweight training (calisthenics) like pushups, pullups, and planks builds excellent functional strength.",
            "Pushups strengthen the chest, shoulders, and triceps; keep your body in a straight line.",
            "Pullups are a premier back-builder. Engage your lats and control your descent.",
            "Planks build isometric core stability; squeeze your abs, glutes, and thighs.",
            "You do not need gym equipment to build a fit body. Calisthenics can be done anywhere.",
            "Modify pushups by placing your knees on the floor if the standard form is too challenging.",
            "If pullups are difficult, use resistance bands for assistance or do negative pullup drops.",
            "Ensure you maintain strict form to prevent shoulder impingement during bodyweight pushes.",
            "Plank variations like side planks target the obliques and improve spinal stability.",
            "Combine pushups, pullups, and squats for a complete full-body home workout routine."
        ]
    },
    {
        "tag": "leg_exercises",
        "bases": [
            "squats form", "how to squat", "squat benefits", "leg squats exercise", "bodyweight squats",
            "lunges form", "leg lunges", "how to lunge", "walking lunges", "lunge benefits",
            "leg workout", "leg exercises routine", "quads glutes hamstrings", "lower body workout"
        ],
        "responses": [
            "Leg workouts build a strong lower body foundation. Key exercises include squats and lunges. {squats_advice}",
            "Squats target the quads, glutes, and hamstrings. Sit back, keep your chest high, and drive up.",
            "Lunges improve single-leg balance and target the glutes and quadriceps.",
            "Train legs 1-2 times per week to stimulate full-body hypertrophy and hormone release.",
            "Keep your knees aligned with your toes during squats to prevent joint strain.",
            "Add weights (dumbbells or barbells) once you master bodyweight squat and lunge form.",
            "Leg exercises like lunges correct strength imbalances between your left and right legs.",
            "A strong lower body improves athletic power, running speed, and daily mobility.",
            "Ensure you warm up your hips and knees thoroughly before initiating leg workouts.",
            "Incorporate hamstring curls and calf raises to build a balanced lower body profile."
        ]
    },
    {
        "tag": "arm_exercises",
        "bases": [
            "bicep curls", "bicep curls form", "dumbbell curls", "arm curls", "grow biceps",
            "arm exercises", "tricep dips", "hammer curls", "tricep extension", "arm workout",
            "bicep training", "tricep training", "bicep curls dumbbell", "arms gym"
        ],
        "responses": [
            "Arm workouts target the biceps, triceps, and forearms. Use bicep curls and tricep dips.",
            "For bicep curls, keep your elbows tucked at your sides and avoid swinging the weights.",
            "Triceps make up 60% of your upper arm size; focus on dips, pushdowns, and overhead extensions.",
            "Ensure you perform a full range of motion, stretching and squeezing the muscle on each rep.",
            "Combine bicep curls and tricep presses for an effective arm pump routine.",
            "Vary dumbbell grips (e.g., hammer curls) to target different areas of the arm muscles.",
            "Arm isolation exercises are best done at the end of your upper body workouts.",
            "Avoid using momentum during bicep curls to ensure the load stays on the bicep fibers.",
            "Strong arms support your compound movements like bench presses and pullups.",
            "Aim for 3-4 sets of 10-15 repetitions for arm hypertrophy exercises."
        ]
    },
    {
        "tag": "abdominal_exercises",
        "bases": [
            "core workout", "ab workout routine", "abs exercises", "six pack training", "strengthen core",
            "crunches form", "situps guide", "oblique exercises", "ab exercises gym", "belly workout",
            "abdominal routine", "ab training", "belly fat exercise", "flat stomach workout"
        ],
        "responses": [
            "Core exercises strengthen the abs, obliques, and lower back. Focus on planks and leg raises.",
            "Crunches isolate the upper abdominals; focus on lifting with your core, not your neck.",
            "Oblique crunches and Russian twists target the rotational core muscles.",
            "A strong abdominal wall protects your spine and improves performance in heavy compound lifts.",
            "Visible abs are built in the gym but revealed through a low body fat percentage (diet).",
            "Incorporate hanging leg raises to target the lower abdominal fibers.",
            "Focus on quality core contraction rather than doing hundreds of mindless crunches.",
            "Avoid daily ab training; treat abdominals like any other muscle and allow rest.",
            "Bicycle crunches are highly rated for activating the rectus abdominis and obliques.",
            "A balanced abdominal routine includes stability holds (planks) and flexion (crunches)."
        ]
    },
    {
        "tag": "weight_issues",
        "bases": [
            "obesity risk", "clinical obesity", "overweight dangers", "managing obesity", "excess body fat",
            "underweight health", "weight gain diet", "how to gain weight", "build body mass",
            "too skinny", "mujhe mota hona hai", "mota hone ki diet", "weight gain tips", "fat issues"
        ],
        "responses": [
            "Weight issues range from underweight to obesity. Managing them requires adjusting caloric intake. {obesity_advice} {underweight_advice}",
            "If underweight, create a caloric surplus with nutrient-dense fats, proteins, and strength training.",
            "If struggling with obesity, aim for a consistent, moderate caloric deficit of 300-500 kcal daily.",
            "Monitor your physical progress using BMI checks, tape measurements, and strength indicators.",
            "Avoid crash diets; sustainable weight loss or gain is a gradual, long-term habit shift.",
            "Focus on clean, whole foods whether you are trying to lose body fat or gain lean mass.",
            "Being underweight can lead to nutritional deficiencies; prioritize nutrient density.",
            "Obesity is associated with metabolic issues; regular physical exercise helps improve insulin sensitivity.",
            "Hinglish users ask: mujhe mota hona hai? Add calories via nuts, dairy, banana, and oats.",
            "Consult a medical professional to design a safe, customized weight management strategy."
        ]
    },
    {
        "tag": "healthy_carb_sources",
        "bases": [
            "oats breakfast", "oatmeal nutritional value", "eating oats", "oats benefits", "rolled oats carbs",
            "banana potassium", "banana energy", "eating banana", "banana carbs", "post workout banana",
            "apple fiber", "eating apples", "apple health benefits", "apple pectin", "apple calories",
            "complex carbohydrates", "healthy carbs", "carbohydrates sources"
        ],
        "responses": [
            "Healthy carb sources include rolled oats, bananas, apples, brown rice, and sweet potatoes. {oats_advice}",
            "Oats provide soluble fiber (beta-glucan) which helps regulate cholesterol and keeps you full.",
            "Bananas are rich in potassium and fast-acting carbs, making them ideal pre-workout fuel.",
            "Apples contain pectin fiber, supporting gut health while keeping your calorie intake low.",
            "Carbohydrates are your body's primary fuel source during intense physical workouts.",
            "Choose complex carbs over refined sugars for sustained energy release without insulin spikes.",
            "A post-workout banana helps replenish muscle glycogen levels quickly.",
            "Oatmeal bowls topped with fruit are perfect to fuel early morning workout sessions.",
            "Apples make a low-calorie, portable snack that aids daily fiber targets.",
            "Balance your macronutrients by matching carbohydrate intake to your physical activity level."
        ]
    },
    {
        "tag": "healthy_protein_foods",
        "bases": [
            "chicken breast", "eating chicken", "chicken protein amount", "chicken macro profile", "cooked chicken breast",
            "eggs protein", "boiled eggs", "whole eggs vs egg whites", "eating eggs nutrition", "egg macronutrients",
            "eating fish", "salmon omega 3", "tuna protein", "healthy fish list", "fish benefits",
            "protein food list", "lean protein foods"
        ],
        "responses": [
            "High-quality protein foods include chicken breast, eggs, and fatty fish (salmon/tuna). {chicken_advice} {eggs_advice} {fish_advice}",
            "Chicken breast is a top lean protein source, supplying 31g of protein per 100g with low fat.",
            "Whole eggs provide highly bioavailable proteins and essential healthy fats in the yolk.",
            "Fatty fish like salmon supply both clean protein and anti-inflammatory Omega-3 fatty acids.",
            "Lean protein supports muscle protein synthesis and promotes satiety during weight loss.",
            "Egg whites are a pure, low-calorie protein source, perfect for strict fat loss diets.",
            "Include fish in your weekly meals to support brain, heart, and joint health.",
            "Chicken breast with sweet potatoes and broccoli is a standard, clean recovery meal.",
            "Consuming a variety of protein foods ensures you get all essential amino acids.",
            "Prepare your proteins via baking, grilling, or boiling rather than deep frying."
        ]
    },
    {
        "tag": "healthy_fat_sources",
        "bases": [
            "avocado fats", "avocado benefits", "eating avocado", "healthy fats avocado", "avocado calorie density",
            "nuts fats", "almonds protein", "eating nuts", "walnuts omega 3", "healthy nuts snack",
            "healthy fats list", "benefits of healthy fats", "fat nutrition source", "almonds walnuts"
        ],
        "responses": [
            "Healthy fat sources include avocados, almonds, walnuts, olive oil, and seeds.",
            "Avocados contain monounsaturated fats that support heart health and nutrient absorption.",
            "Almonds and walnuts deliver healthy fats, dietary fiber, and plant-based protein.",
            "Fats are essential for hormone production, joint lubrication, and brain function.",
            "Healthy fats are calorie-dense (9 kcal/g), so manage portion sizes to avoid excess calories.",
            "Walnuts are a great source of plant-based omega-3 alpha-linolenic acid (ALA).",
            "Use extra virgin olive oil as a healthy dressing for salads and cooked meals.",
            "Eating healthy fats keeps you feeling satisfied and prevents excessive snacking.",
            "Avoid trans fats and limit saturated fats; prioritize unsaturated fat sources instead.",
            "Add avocado slices to your breakfast eggs to build a balanced macro profile."
        ]
    },
    {
        "tag": "healthy_greens",
        "bases": [
            "eating salads", "healthy salad recipe", "salad for weight loss", "salad nutrition", "green salad vegetable",
            "broccoli nutrition", "eating broccoli", "broccoli vitamins", "cruciferous broccoli", "steamed broccoli",
            "spinach iron", "eating spinach", "spinach benefits", "leafy green spinach", "raw spinach salad",
            "greek yogurt", "yogurt probiotics", "eating yogurt", "yogurt protein amount", "curd benefits"
        ],
        "responses": [
            "Healthy greens and probiotic foods include spinach, broccoli, salad greens, and Greek yogurt. {salad_advice} {broccoli_advice}",
            "Spinach is loaded with iron, calcium, and magnesium to support blood and bone health.",
            "Broccoli is a cruciferous vegetable high in vitamin C and fiber, protecting cells.",
            "Greek yogurt provides probiotics for gut health along with highly bioavailable protein.",
            "Green salad bowls add substantial volume to your meals with negligible calories.",
            "Steaming broccoli preserves its micronutrients better than boiling or frying.",
            "Spinach can be easily blended into your protein shakes for a nutrient boost.",
            "Yogurt and green vegetables support a healthy microbiome, aiding digestion.",
            "A daily salad with spinach, cucumber, and broccoli supports fat loss goals.",
            "Add curd or Greek yogurt to your meals to support digestive health and calcium needs."
        ]
    },
    {
        "tag": "fallback",
        "bases": [
            "unsure", "i do not know", "random query", "non fitness question", "what is the capital of france",
            "who is the president", "tell me a joke", "play some music", "stock market price",
            "not clear", "what is 2 plus 2", "weather today", "do you know math", "talk about movies"
        ],
        "responses": [
            "I'm not completely sure what you mean. Are you asking about:\n• Workouts (beginner, fat loss, muscle gain)\n• Nutrition (meal plans, protein sources, healthy fats)\n• BMI checks or Daily Calories\n• Sleep and Hydration targets\n• Stretching and Yoga?",
            "I didn't quite catch that fitness query. Would you like to explore:\n• Guided Workouts\n• Dietary Patterns (Keto, Vegan)\n• BMR and Calorie Calculations\n• Daily Water Intake Goals\n• Stress and Sleep Recovery?",
            "I specialize in health and fitness topics. Please clarify if you are asking about:\n• Strength Training and Cardio\n• BMI and Weight Categories\n• Healthy Food Items (Oats, Chicken, Eggs)\n• Mobility and Flexibility\n• Fitness Motivation?",
            "That query seems outside my health scope. Please ask me about:\n• How to calculate your BMI\n• Healthy meals for breakfast, lunch, or dinner\n• Exercises like squats, pushups, and planks\n• How much sleep or water you require\n• Consistently staying motivated?",
            "I'm here as your HealthFit AI Assistant. Let's redirect to:\n• Workouts (HIIT, Core, Lower Body)\n• Calorie budgeting and TDEE\n• Lean protein and carb sources\n• Stress relief and yoga poses\n• Physical metrics tracking?",
            "I didn't understand that. Please specify if you want advice on:\n• Losing weight or gaining muscle\n• Beginners starting at the gym\n• Healthy snacks and leafy greens\n• Upper body and arm routines\n• Stretching sore muscles?",
            "That topic is outside my expertise. Try asking about:\n• Weight and height BMI checks\n• Basal Metabolic Rate (BMR) estimates\n• Lean protein and healthy fats\n• Rest and recovery durations\n• Simple bodyweight exercises?",
            "I'm optimized for wellness queries. Let me know if you need help with:\n• Hydration (daily water targets)\n• Sleep (hours needed for recovery)\n• Healthy breakfast, lunch, and dinners\n• Exercises (bench press, lunges, curls)\n• Dietary templates (Keto, Vegan)?",
            "Let's focus on your physical fitness. Are you interested in:\n• Beginner training structures\n• Muscle building routines\n• Fat loss cardio sessions\n• Yoga and flexibility poses\n• Daily calorie budgets?",
            "I'm not sure how to answer that. Let's discuss: workouts, nutrition, BMI score, hydration daily limits, or sleep guidelines!"
        ]
    },
    {
        "tag": "emergency_disclaimer",
        "bases": [
            "chest pain", "heart attack", "difficulty breathing", "injury hurt", "medical emergency",
            "doctor hospital", "injured bleeding", "broken bone", "severely hurt", "chest tightening",
            "dizzy fainting", "call ambulance", "emergency helpline", "accident blood", "hospital emergency"
        ],
        "responses": [
            "WARNING: If you are experiencing chest pain, severe shortness of breath, or sudden dizziness, please contact emergency medical services immediately.",
            "Safety first: If you have a severe injury or are in physical distress, stop exercising and call a doctor.",
            "I am an AI assistant, not a doctor. In case of a medical emergency, please visit the nearest hospital.",
            "If you feel sudden pain or breathlessness while working out, halt immediately and seek professional care.",
            "For any sudden health complications, always contact qualified medical emergency providers.",
            "If you suspect a heart attack or stroke, dial your local emergency number (e.g., 911 or 112) now.",
            "Do not ignore chest tightness or severe pain. Please consult a physician immediately.",
            "My advice is for general fitness only. For emergency symptoms, seek clinical care immediately.",
            "If you are bleeding or have a suspected fracture, contact hospital emergency departments.",
            "In case of any acute, severe physical discomfort, contact emergency medical professionals without delay."
        ]
    }
]


def expand_patterns(bases: list) -> list:
    """Expand bases using PREFIXES to generate at least 80 unique patterns."""
    patterns = set()
    for base in bases:
        patterns.add(base)
        patterns.add(base + "s")
        patterns.add(base + "ing")
        for pref in PREFIXES:
            patterns.add((pref + base).strip())
            patterns.add((pref + "a " + base).strip())
            patterns.add((pref + "some " + base).strip())
            
    # Convert to list and sort to be deterministic
    lst = sorted(list(patterns))
    return lst


def generate_dataset():
    """Generates intents.json, enforcing exactly 75 patterns per intent."""
    intents_list = []
    total_patterns = 0

    print("Generating balanced dataset blueprints...")

    for bp in BLUEPRINTS:
        tag = bp["tag"]
        bases = bp["bases"]
        responses = bp["responses"]

        # Expand patterns
        expanded = expand_patterns(bases)
        
        # Always include the clean base phrases first to prevent core classification failure
        final_patterns = set(bases)
        
        # Get all other unique variations
        variations = [p for p in expanded if p not in final_patterns]
        
        if len(final_patterns) < 75:
            needed = 75 - len(final_patterns)
            random.seed(tag)
            if len(variations) >= needed:
                selected_vars = random.sample(variations, needed)
                final_patterns.update(selected_vars)
            else:
                final_patterns.update(variations)
                # If still not enough, pad with minor variations
                pad_idx = 0
                while len(final_patterns) < 75:
                    base = bases[pad_idx % len(bases)]
                    var = f"{base}?" if pad_idx % 2 == 0 else f"please {base}"
                    final_patterns.add(var)
                    pad_idx += 1
        elif len(final_patterns) > 75:
            # If bases themselves exceed 75, sample from bases
            random.seed(tag)
            final_patterns = set(random.sample(list(final_patterns), 75))

        final_patterns_list = sorted(list(final_patterns))
        total_patterns += len(final_patterns_list)

        intents_list.append({
            "tag": tag,
            "patterns": final_patterns_list,
            "responses": responses
        })

    # Wrap in final structure
    dataset = {"intents": intents_list}

    # Save to disk
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Dataset successfully compiled!")
    print(f"Total Intents : {len(intents_list)}")
    print(f"Total Patterns: {total_patterns} (exactly 75 per intent)")
    print(f"Output File   : {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dataset()
