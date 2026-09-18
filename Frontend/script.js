// Point this to your FastAPI backend server
const API_BASE_URL = "https://sih26091-team-arthx.onrender.com";

// Language Voice / Speech Synthesis BCP-47 locale map
const langVoiceMap = {
  en: "en-IN",
  hi: "hi-IN",
  mr: "mr-IN",
  gu: "gu-IN",
  bn: "bn-IN",
  ta: "ta-IN",
  te: "te-IN",
  kn: "kn-IN"
};

// Comprehensive Multi-Language Dictionary
const i18n = {
  en: {
    tagline: "Smart business funding, in plain words",
    loginSignupBtn: "Sign Up / Login",
    logoutBtn: "Logout",
    heroEyebrow: "For village and small-town entrepreneurs",
    heroTitle: "Turn your savings into a funded business plan.",
    heroSub: "Tell us your location and available cash. We calculate your total budget, map local competitors, and match you with government schemes.",
    flowTitle: "How ArthSaarthak Works",
    flow1: "Input Details & Margin Capital",
    flow2: "AI Analyzes Market & Calculates Loan (90%)",
    flow3: "Get Scheme Match & EMI Plan",
    wizardTitle: "Business & Location Setup",
    step1Label: "1. Personal & Contact Details",
    phFullName: "Full Name",
    phPhone: "Phone Number",
    step2Label: "2. Granular Location & Area Type",
    ruralBtn: "Village / Gram Panchayat",
    urbanBtn: "Town / City",
    phState: "State (e.g. Uttar Pradesh)",
    phDistrict: "District",
    phBlock: "Block / Tehsil",
    phVillage: "Village / City Name",
    loadingVillages: "Loading seeded villages…",
    otherNotListed: "Other / Not listed (enter manually below)",
    unseededHint: "This location isn't in our seeded data yet — your loan & scheme report will still work, but live competitor, mandi price, and target audience insights won't be available for it.",
    q2: "3. Business Category",
    catDairy: "Dairy Farming",
    catTailor: "Tailoring",
    catGrocery: "Grocery Store",
    q3: "4. Your Margin Capital (₹)",
    phMargin: "e.g. 50000",
    calcBtn: "Generate AI Report",
    reportTitle: "Your Business & Financial Report",
    listenBtn: "Listen",
    downloadBtn: "Download / Print",
    docsTitle: "Required Documents Checklist",
    docsHint: "Keep these ready before visiting the local bank or Common Service Center (CSC).",
    docPhoto: "Passport Size Photographs (2)",
    docId: "Identity Proof (Aadhaar/Voter ID/PAN)",
    docAddr: "Address Proof (Electricity Bill/Ration Card)",
    docQuote: "Quotation of Machinery / Equipment",
    docReport: "Project Report (ArthSaarthak AI Report)",
    errorServer: "Could not connect to the server.",
    journalTitle: "Business Journal & Tracking",
    journalSub: "Log your daily sales and ask your ledger a question, anytime.",
    jnlLogTitle: "Log Daily Entry",
    phSales: "Sales Revenue (₹)",
    phExpenses: "Expenses (₹)",
    phUnits: "Units Sold (Optional)",
    jnlSaveBtn: "Save Entry",
    jnlSaveStatus: "Saved successfully!",
    jnlAskTitle: "Ask Your Ledger",
    jnlAskHint: "e.g. 'What was my highest sales day?' or 'Show total expenses.'",
    phJnlQuery: "Ask AI about records...",
    jnlAskBtn: "Ask Ledger AI",
    jnlRecordsTitle: "Recent Ledger Records",
    jnlRefreshBtn: "Refresh Table",
    thDate: "Date",
    thSales: "Sales (₹)",
    thExpenses: "Expenses (₹)",
    thUnits: "Units Sold",
    jnlEmptyState: "Click 'Refresh Table' to load entries.",
    toolsTitle: "Financial Engines",
    toolsSub: "Stress-test your business before you borrow a single rupee.",
    simCardTitle: "AI Survival Simulator",
    simCardDesc: "Test your business resilience against market shocks and seasonal demand drops.",
    openSimBtn: "Open Simulator",
    scenarioCardTitle: "Scenario & Pricing Planner",
    scenarioCardDesc: "Compare base plans against optimized pricing models to lower breakeven points.",
    runScenarioBtn: "Run Scenario Check",
    ftUdyam: "Udyam Registration", ftUdyamSub: "Official MSME registration portal.",
    ftPmegp: "PMEGP Portal", ftPmegpSub: "Credit-linked subsidy schemes.",
    ftMudra: "Mudra Loans", ftMudraSub: "Collateral-free institutional credit.",
    ftHelpline: "Ministry Helpline", ftHelpSub: "MSME Helpdesk:", ftVisit: "Visit Portal ↗", ftMinistry: "Visit Ministry ↗",
    navHome: "Home", navJournal: "Journal", navTools: "Tools", navChat: "Chat",
    chatTitle: "Talk to our AI Assistant",
    chatGreeting: "Hello! Tell me about your business idea and how much money you have to start.",
    chatInputPlaceholder: "Type or speak here...",
    sendBtn: "Send",
    tabLogin: "Login", tabSignup: "Sign Up", loginHeading: "Welcome Back", signupHeading: "Create an Account",
    phEmail: "Email Address", phPassword: "Password", phCreatePass: "Create Password",
    simModalTitle: "AI Business Survival Simulator", simModalDesc: "Simulate 1,000 seasonal variations to estimate your 12-month survival rate.",
    simLabelCash: "Initial Capital (₹)", simPlaceholderCash: "e.g. 50000",
    simLabelRev: "Monthly Revenue (₹)", simPlaceholderRev: "e.g. 30000",
    simLabelExp: "Monthly Expenses (₹)", simPlaceholderExp: "e.g. 18000",
    simLabelEmi: "Monthly EMI (₹)", simPlaceholderEmi: "e.g. 4500",
    simulating: "Simulating 1,000 market conditions...",
    simResults: "Simulation Results",
    simSurvival: "Survival Probability",
    simRisk: "Risk Level",
    simTested: "Tested across",
    simCycles: "randomized seasonal demand cycles.",
    simFail: "Simulation engine failed to connect. Ensure backend is running.",
    runSimBtn: "Run Simulations"
  },
  hi: {
    tagline: "स्मार्ट व्यापार फंडिंग, सरल शब्दों में",
    loginSignupBtn: "साइन अप / लॉगिन",
    logoutBtn: "लॉगआउट",
    heroEyebrow: "गांव और छोटे शहर के उद्यमियों के लिए",
    heroTitle: "अपनी बचत को एक वित्तपोषित व्यवसाय योजना में बदलें।",
    heroSub: "हमें अपना स्थान और उपलब्ध नकद बताएं। हम आपके कुल बजट की गणना करते हैं और आपको सरकारी योजनाओं से मिलाते हैं।",
    flowTitle: "अर्थसार्थक कैसे काम करता है",
    flow1: "विवरण और मार्जिन पूंजी दर्ज करें",
    flow2: "AI बाजार का विश्लेषण करता है और ऋण की गणना करता है (90%)",
    flow3: "योजना मिलान और EMI योजना प्राप्त करें",
    wizardTitle: "व्यवसाय और स्थान सेटअप",
    step1Label: "1. व्यक्तिगत और संपर्क विवरण",
    phFullName: "पूरा नाम",
    phPhone: "फोन नंबर",
    step2Label: "2. स्थान का प्रकार",
    ruralBtn: "गांव / ग्राम पंचायत",
    urbanBtn: "शहर / नगर",
    phState: "राज्य (जैसे उत्तर प्रदेश)",
    phDistrict: "ज़िला",
    phBlock: "ब्लॉक / तहसील",
    phVillage: "गांव / शहर का नाम",
    q2: "3. व्यवसाय श्रेणी",
    catDairy: "डेयरी फार्मिंग",
    catTailor: "सिलाई / टेलरिंग",
    catGrocery: "किराने की दुकान",
    q3: "4. आपकी मार्जिन पूंजी (₹)",
    phMargin: "जैसे 50000",
    calcBtn: "AI रिपोर्ट जनरेट करें",
    reportTitle: "आपकी व्यावसायिक और वित्तीय रिपोर्ट",
    listenBtn: "सुनें",
    downloadBtn: "डाउनलोड / प्रिंट करें",
    docsTitle: "आवश्यक दस्तावेजों की जांच सूची",
    docsHint: "स्थानीय बैंक या कॉमन सर्विस सेंटर (CSC) जाने से पहले इन्हें तैयार रखें।",
    docPhoto: "पासपोर्ट आकार की तस्वीरें (2)",
    docId: "पहचान पत्र (आधार/वोटर आईडी/पैन)",
    docAddr: "पते का प्रमाण (बिजली बिल/राशन कार्ड)",
    docQuote: "मशीनरी/उपकरण का कोटेशन",
    docReport: "प्रोजेक्ट रिपोर्ट (अर्थसार्थक AI रिपोर्ट)",
    errorServer: "सर्वर से कनेक्ट नहीं हो सका।",
    journalTitle: "व्यावसायिक जर्नल और ट्रैकिंग",
    journalSub: "अपनी दैनिक बिक्री दर्ज करें और किसी भी समय लेजर से प्रश्न पूछें।",
    jnlLogTitle: "दैनिक प्रविष्टि दर्ज करें",
    phSales: "बिक्री राजस्व (₹)",
    phExpenses: "खर्च (₹)",
    phUnits: "बेची गई इकाइयाँ (वैकल्पिक)",
    jnlSaveBtn: "प्रविष्टि सहेजें",
    jnlSaveStatus: "सफलतापूर्वक सहेजा गया!",
    jnlAskTitle: "अपने लेजर से पूछें",
    jnlAskHint: "जैसे 'मेरी सबसे ज्यादा बिक्री किस दिन हुई?' या 'कुल खर्च दिखाएं।'",
    phJnlQuery: "रिकॉर्ड के बारे में AI से पूछें...",
    jnlAskBtn: "लेजर AI से पूछें",
    jnlRecordsTitle: "हालिया लेजर रिकॉर्ड",
    jnlRefreshBtn: "तालिका ताज़ा करें",
    thDate: "तिथि",
    thSales: "बिक्री (₹)",
    thExpenses: "खर्च (₹)",
    thUnits: "बेची गई इकाइयाँ",
    jnlEmptyState: "प्रविष्टियाँ लोड करने के लिए 'तालिका ताज़ा करें' पर क्लिक करें।",
    toolsTitle: "वित्तीय इंजन",
    toolsSub: "एक भी रुपया उधार लेने से पहले अपने व्यवसाय का परीक्षण करें।",
    simCardTitle: "AI सर्वाइवल सिमुलेटर",
    simCardDesc: "बाजार के झटकों और मौसमी मांग में गिरावट के खिलाफ अपनी व्यावसायिक क्षमता का परीक्षण करें।",
    openSimBtn: "सिमुलेटर खोलें",
    scenarioCardTitle: "परिदृश्य और मूल्य निर्धारण योजनाकार",
    scenarioCardDesc: "ब्रेकईवन पॉइंट कम करने के लिए इष्टतम मूल्य निर्धारण मॉडल से तुलना करें।",
    runScenarioBtn: "परिदृश्य जांच चलाएं",
    ftUdyam: "उद्यम पंजीकरण", ftUdyamSub: "आधिकारिक MSME पंजीकरण पोर्टल।",
    ftPmegp: "PMEGP पोर्टल", ftPmegpSub: "क्रेडिट-लिंक्ड सब्सिडी योजनाएं।",
    ftMudra: "मुद्रा ऋण", ftMudraSub: "संपार्श्विक-मुक्त संस्थागत ऋण।",
    ftHelpline: "मंत्रालय हेल्पलाइन", ftHelpSub: "MSME हेल्पडेस्क:", ftVisit: "पोर्टल पर जाएं ↗", ftMinistry: "मंत्रालय पर जाएं ↗",
    navHome: "होम", navJournal: "जर्नल", navTools: "टूल्स", navChat: "चैट",
    chatTitle: "हमारे AI सहायक से बात करें",
    chatGreeting: "नमस्ते! मुझे अपने व्यावसायिक विचार और अपने बजट के बारे में बताएं।",
    chatInputPlaceholder: "यहाँ टाइप करें या बोलें...",
    sendBtn: "भेजें",
    tabLogin: "लॉगिन", tabSignup: "साइन अप", loginHeading: "वापसी पर स्वागत है", signupHeading: "खाता बनाएं",
    phEmail: "ईमेल पता", phPassword: "पासवर्ड", phCreatePass: "पासवर्ड बनाएं",
    simModalTitle: "AI व्यापार उत्तरजीविता सिमुलेटर", simModalDesc: "12 महीने की उत्तरजीविता दर का अनुमान लगाने के लिए 1,000 मौसमी विविधताओं का सिमुलेशन करें।",
    simLabelCash: "प्रारंभिक पूंजी (₹)", simPlaceholderCash: "जैसे 50000",
    simLabelRev: "मासिक राजस्व (₹)", simPlaceholderRev: "जैसे 30000",
    simLabelExp: "मासिक खर्च (₹)", simPlaceholderExp: "जैसे 18000",
    simLabelEmi: "मासिक EMI (₹)", simPlaceholderEmi: "जैसे 4500",
    simulating: "1,000 बाजार स्थितियों का सिमुलेशन किया जा रहा है...",
    simResults: "सिमुलेशन परिणाम",
    simSurvival: "अस्तित्व की संभावना",
    simRisk: "जोखिम स्तर",
    simTested: "परीक्षण किया गया",
    simCycles: "यादृच्छिक मौसमी मांग चक्रों में।",
    simFail: "सिमुलेशन इंजन कनेक्ट होने में विफल रहा। सुनिश्चित करें कि बैकएंड चल रहा है।",
    runSimBtn: "सिमुलेशन चलाएं"
  },
  mr: {
    tagline: "स्मार्ट व्यवसाय निधी, सोप्या शब्दात",
    loginSignupBtn: "साइन अप / लॉगिन", logoutBtn: "लॉगआउट",
    heroEyebrow: "ग्रामीण आणि लहान शहरातील उद्योजकांसाठी",
    heroTitle: "तुमच्या बजेटला व्यवसाय योजनेत बदला.",
    heroSub: "तुमचे स्थान आणि उपलब्ध भांडवल सांगा. आम्ही तुमचे बजेट, स्थानिक स्पर्धक आणि सरकारी योजना शोधून देऊ.",
    flowTitle: "अर्थसार्थक कसे काम करते", flow1: "माहिती भरा", flow2: "AI बाजार विश्लेषण", flow3: "योजना व EMI मिळवा",
    wizardTitle: "व्यवसाय आणि स्थान तपशील", step1Label: "१. वैयक्तिक माहिती", phFullName: "पूर्ण नाव", phPhone: "फोन नंबर",
    step2Label: "२. स्थान प्रकार", ruralBtn: "ग्रामीण", urbanBtn: "शहरी", phState: "राज्य", phDistrict: "जिल्हा", phBlock: "तालुका", phVillage: "गाव / शहर",
    q2: "३. व्यवसाय प्रकार", catDairy: "डेअरी", catTailor: "शिंपी काम", catGrocery: "किराणा दुकान",
    q3: "४. तुमची भांडवल रक्कम (₹)", phMargin: "उदा. ५००००", calcBtn: "AI रिपोर्ट तयार करा",
    reportTitle: "व्यवसाय आणि आर्थिक अहवाल", listenBtn: "ऐका", downloadBtn: "डाउनलोड / प्रिंट करा",
    docsTitle: "आवश्यक कागदपत्रे", docsHint: "बँकेत जाण्यापूर्वी हे तयार ठेवा.", docPhoto: "पासपोर्ट फोटो (२)", docId: "ओळखपत्र (आधार/पॅन)", docAddr: "पत्ता पुरावा", docQuote: "मशीनरी कोटेशन", docReport: "प्रकल्प अहवाल",
    errorServer: "सर्व्हरशी संपर्क होऊ शकला नाही.",
    journalTitle: "व्यवसाय नोंदवही", journalSub: "दैनिक विक्री नोंदवा आणि प्रश्न विचारा.", jnlLogTitle: "दैनंदिन नोंद करा", phSales: "विक्री (₹)", phExpenses: "खर्च (₹)", phUnits: "नग", jnlSaveBtn: "जतन करा", jnlSaveStatus: "जतन केले!", jnlAskTitle: "लेजरला विचारा", jnlAskHint: "उदा. 'एकूण खर्च किती झाला?'", phJnlQuery: "प्रश्न विचारा...", jnlAskBtn: "विचारा", jnlRecordsTitle: "अलिकडील नोंदी", jnlRefreshBtn: "रिफ्रेश करा", thDate: "दिनांक", thSales: "विक्री (₹)", thExpenses: "खर्च (₹)", thUnits: "विकलेले नग", jnlEmptyState: "नोंदी पाहण्यासाठी रिफ्रेश करा.",
    toolsTitle: "आर्थिक साधने", toolsSub: "कर्ज घेण्यापूर्वी व्यवसायाची चाचणी घ्या.", simCardTitle: "AI सर्व्हायव्हल सिम्युलेटर", simCardDesc: "बाजारपेठेतील चढ-उतारांची चाचणी घ्या.", openSimBtn: "सिम्युलेटर उघडा", scenarioCardTitle: "किंमत नियोजक", scenarioCardDesc: "नफ्याचे विश्लेषण करा.", runScenarioBtn: "तपासा",
    ftUdyam: "उद्योग नोंदणी", ftUdyamSub: "अधिकृत MSME पोर्टल.", ftPmegp: "PMEGP पोर्टल", ftPmegpSub: "अनुदान योजना.", ftMudra: "मुद्रा कर्ज", ftMudraSub: "विनातारण कर्ज.", ftHelpline: "हेल्पलाइन", ftHelpSub: "MSME मदत:", ftVisit: "पोर्टल पहा ↗", ftMinistry: "मंत्रालय ↗",
    navHome: "मुख्य", navJournal: "नोंदवही", navTools: "साधने", navChat: "चॅट",
    chatTitle: "AI सहाय्यकाशी बोला", chatGreeting: "नमस्कार! तुमच्या व्यवसायाबद्दल सांगा.", chatInputPlaceholder: "येथे टाईप करा...", sendBtn: "पाठवा",
    tabLogin: "लॉगिन", tabSignup: "साइन अप", loginHeading: "पुन्हा स्वागत आहे", signupHeading: "खाते उघडा", phEmail: "ईमेल", phPassword: "पासवर्ड", phCreatePass: "पासवर्ड तयार करा",
    simModalTitle: "AI व्यवसाय सिम्युलेटर", simModalDesc: "१२ महिन्यांच्या स्थिरतेची चाचणी घ्या.", simLabelCash: "प्रारंभिक भांडवल (₹)", simPlaceholderCash: "५००००", simLabelRev: "मासिक उत्पन्न (₹)", simPlaceholderRev: "३००००", simLabelExp: "मासिक खर्च (₹)", simPlaceholderExp: "१८०००", simLabelEmi: "मासिक हप्ता (₹)", simPlaceholderEmi: "४५००",
    simulating: "सिम्युलेशन सुरू आहे...", simResults: "निकाल", simSurvival: "यशस्वी होण्याची शक्यता", simRisk: "जोखीम पातळी", simTested: "परीक्षण केले", simCycles: "हंगामी बाजाराच्या आधारे.", simFail: "जोडणी अयशस्वी.", runSimBtn: "सिम्युलेशन चालवा"
  }
};

let currentLang = 'en';

// Master Helper function for translational Lookup
function t(key) {
  const activeDict = i18n[currentLang] || i18n['en'];
  return activeDict[key] || i18n['en'][key] || key;
}

// Master Language Switcher & Universal DOM Translator
function updateLanguage(langKey) {
  currentLang = langKey;
  const selectedDict = i18n[currentLang] || i18n['en'];
  const fallbackDict = i18n['en'];

  // 1. Translate innerText / innerHTML for elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    const translation = selectedDict[key] || fallbackDict[key];
    if (translation) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = translation;
      } else {
        el.innerHTML = translation;
      }
    }
  });

  // 2. Translate placeholders for elements with data-i18n-ph
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    const key = el.getAttribute("data-i18n-ph");
    const translation = selectedDict[key] || fallbackDict[key];
    if (translation) {
      el.placeholder = translation;
    }
  });
}

// Global Application Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupLanguage();
  setupUI();
  setupVoice();
  updateLanguage(currentLang);
});

function setupLanguage() {
  const langSelect = document.getElementById("langSelect");
  if (langSelect) {
    langSelect.addEventListener("change", (e) => {
      updateLanguage(e.target.value);
    });
  }
}

function setupUI() {
  // Navigation Bar Logic
  const navItems = document.querySelectorAll(".bottom-nav .nav-item[data-view]");
  const views = document.querySelectorAll(".app-view");

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetView = item.getAttribute("data-view");
      navItems.forEach(i => i.classList.remove("active"));
      item.classList.add("active");

      views.forEach(v => {
        if (v.id === `view-${targetView}`) {
          v.classList.add("active-view");
        } else {
          v.classList.remove("active-view");
        }
      });
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Toggle button styling for Area Type (Rural vs Urban)
  document.querySelectorAll(".toggle-row .pill-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".toggle-row .pill-btn").forEach(b => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", "true");
    });
  });

  // Event Listeners for primary buttons
  document.getElementById("calcBtn")?.addEventListener("click", submitWizardToFastAPI);
  document.getElementById("chatBtn")?.addEventListener("click", submitChatToFastAPI);
  document.getElementById("downloadBtn")?.addEventListener("click", () => window.print());
  
  const readBtn = document.getElementById("readAloudBtn");
  if (readBtn) readBtn.addEventListener("click", readReportAloud);
  
  const logBtn = document.getElementById("logJournalBtn");
  if (logBtn) logBtn.addEventListener("click", submitJournalEntry);
  
  const askBtn = document.getElementById("askJournalBtn");
  if (askBtn) askBtn.addEventListener("click", askJournal);

  const loadEntriesBtn = document.getElementById("loadEntriesBtn");
  if (loadEntriesBtn) loadEntriesBtn.addEventListener("click", fetchJournalEntries);

  const dateEl = document.getElementById("journalDate");
  if (dateEl) dateEl.valueAsDate = new Date();

  loadSeededLocations();
  document.getElementById("stateSelect")?.addEventListener("change", handleStateSelectChange);
  document.getElementById("districtSelect")?.addEventListener("change", handleDistrictSelectChange);
  document.getElementById("blockSelect")?.addEventListener("change", handleBlockSelectChange);
  document.getElementById("villageSelectSeed")?.addEventListener("change", handleVillageSelectSeedChange);

  const manualToggleBtn = document.getElementById("manualLocationToggle");
  if (manualToggleBtn) {
    manualToggleBtn.addEventListener("click", () => {
      const isManualHidden = document.getElementById("manualLocationGroup").style.display === "none";
      if (isManualHidden) {
        showManualLocationFallback();
        manualToggleBtn.textContent = "Use seeded location list instead";
      } else {
        hideManualLocationFallback();
        manualToggleBtn.textContent = "My village/town isn't listed — enter manually";
      }
    });
  }

  // Floating Chat Toggle Logic
  const chatToggleBtn = document.getElementById("chatToggleBtn");
  const navChatBtn = document.getElementById("navChatBtn");
  const floatingChatWidget = document.getElementById("floatingChatWidget");
  const closeChatBtn = document.getElementById("closeChatBtn");

  const openChat = () => {
    if (floatingChatWidget) floatingChatWidget.classList.remove("hidden");
    if (chatToggleBtn) chatToggleBtn.style.display = "none";
  };

  const closeChat = () => {
    if (floatingChatWidget) floatingChatWidget.classList.add("hidden");
    if (chatToggleBtn) chatToggleBtn.style.display = "flex";
  };

  if (chatToggleBtn) chatToggleBtn.addEventListener("click", openChat);
  if (navChatBtn) navChatBtn.addEventListener("click", openChat);
  if (closeChatBtn) closeChatBtn.addEventListener("click", closeChat);

  // Authentication Modal Logic
  const authModal = document.getElementById("authModal");
  const openAuthBtn = document.getElementById("openAuthModalBtn");
  const closeAuthBtn = document.getElementById("closeAuthModalBtn");
  const logoutBtn = document.getElementById("logoutBtn");
  const tabBtns = document.querySelectorAll(".auth-tabs .tab-btn");
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");

  if (openAuthBtn && authModal) {
    openAuthBtn.addEventListener("click", () => authModal.classList.remove("hidden"));
    if (closeAuthBtn) closeAuthBtn.addEventListener("click", () => authModal.classList.add("hidden"));
    
    tabBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        tabBtns.forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        const targetTab = e.target.getAttribute("data-tab");
        if (targetTab === "login") {
          loginForm.classList.remove("hidden");
          signupForm.classList.add("hidden");
        } else {
          signupForm.classList.remove("hidden");
          loginForm.classList.add("hidden");
        }
      });
    });

    if (loginForm) {
      loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        authModal.classList.add("hidden");
        if (openAuthBtn) openAuthBtn.classList.add("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");
        alert("Logged in successfully!");
      });
    }

    if (signupForm) {
      signupForm.addEventListener("submit", (e) => {
        e.preventDefault();
        authModal.classList.add("hidden");
        if (openAuthBtn) openAuthBtn.classList.add("hidden");
        if (logoutBtn) logoutBtn.classList.remove("hidden");
        alert("Account created successfully!");
      });
    }

    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        logoutBtn.classList.add("hidden");
        if (openAuthBtn) openAuthBtn.classList.remove("hidden");
        alert("Logged out successfully!");
      });
    }
  }

  // AI Survival Simulator Engine Modal Logic
  const openSimBtn = document.getElementById("openSimModalBtn");
  const simModal = document.getElementById("simModalOverlay");
  const closeSimBtn = document.getElementById("closeSimModalBtn");
  const runSimBtn = document.getElementById("runSimBtn");

  if (openSimBtn && simModal) {
    openSimBtn.addEventListener("click", () => simModal.classList.remove("hidden"));
    if (closeSimBtn) closeSimBtn.addEventListener("click", () => simModal.classList.add("hidden"));
  }

  if (runSimBtn) {
    runSimBtn.addEventListener("click", async () => {
      const payload = {
        initial_cash: parseFloat(document.getElementById("simInitialCash").value) || 0,
        base_monthly_revenue: parseFloat(document.getElementById("simMonthlyRev").value) || 0,
        base_monthly_expenses: parseFloat(document.getElementById("simMonthlyExp").value) || 0,
        emi: parseFloat(document.getElementById("simEmi").value) || 0,
        iterations: 1000
      };

      const resultBox = document.getElementById("simulationResult");
      resultBox.style.display = "block";
      resultBox.innerHTML = `<em>${t('simulating')}</em>`;

      try {
        const response = await fetch(`${API_BASE_URL}/simulate/survival`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await response.json();

        let badgeColor = data.survival_probability_pct > 80 ? '#10B981' : (data.survival_probability_pct > 50 ? '#F59E0B' : '#EF4444');

        resultBox.innerHTML = `
          <h4 style="margin: 0 0 8px 0; color: #1E293B;">${t('simResults')}</h4>
          <p style="margin: 4px 0;">${t('simSurvival')}: <strong style="color: ${badgeColor}; font-size: 16px;">${data.survival_probability_pct}%</strong></p>
          <p style="margin: 4px 0;">${t('simRisk')}: <strong>${data.risk_level}</strong></p>
          <p style="font-size: 12px; color: #64748B; margin-top: 6px;">${t('simTested')} ${data.simulated_iterations} ${t('simCycles')}</p>
        `;
      } catch (e) {
        resultBox.innerHTML = `<span style="color:red">${t('simFail')}</span>`;
      }
    });
  }

  // Scenario Comparison Engine Logic
  const compareBtn = document.getElementById("compareScenariosBtn");
  if (compareBtn) {
    compareBtn.addEventListener("click", async () => {
      const resultBox = document.getElementById("scenarioResultBox");
      resultBox.style.display = "block";
      resultBox.innerHTML = "<em>Running scenario matrix...</em>";

      const payload = {
        base_inputs: {
          project_cost: 1000000,
          margin_pct: 0.10,
          annual_rate_pct: 8.0,
          tenure_months: 84,
          fixed_costs: 50000,
          price_per_unit: 100,
          variable_cost_per_unit: 60
        },
        scenarios: {
          scenario_a: { price_per_unit: 100 },
          scenario_b: { price_per_unit: 120 }
        }
      };

      try {
        const response = await fetch(`${API_BASE_URL}/scenarios/compare`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await response.json();

        resultBox.innerHTML = `
          <h4 style="margin: 0 0 8px 0;">Comparison Results (Breakeven Analysis)</h4>
          <p style="margin: 4px 0;">Base Scenario (₹100/unit): <strong>${data.scenario_a?.breakeven_units || 'N/A'} units</strong></p>
          <p style="margin: 4px 0;">Optimized Scenario (₹120/unit): <strong style="color: #10B981;">${data.scenario_b?.breakeven_units || 'N/A'} units</strong> (Lower breakeven point due to higher margin per unit).</p>
        `;
      } catch (e) {
        resultBox.innerHTML = `<span style="color:red">Failed to fetch scenario comparison from backend.</span>`;
      }
    });
  }
}

// Web Speech Voice Recognition
function setupVoice() {
  const voiceBtn = document.getElementById("voiceBtn");
  const chatInput = document.getElementById("chatInput");
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    if (voiceBtn) voiceBtn.style.display = 'none';
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  
  if (voiceBtn) {
    voiceBtn.addEventListener("click", () => {
      recognition.lang = langVoiceMap[currentLang] || 'en-IN'; 
      recognition.start();
      voiceBtn.classList.add("listening");
    });
  }
  
  recognition.onresult = (event) => {
    chatInput.value = event.results[0][0].transcript;
    if (voiceBtn) voiceBtn.classList.remove("listening");
  };
  recognition.onerror = () => { if (voiceBtn) voiceBtn.classList.remove("listening"); };
  recognition.onend = () => { if (voiceBtn) voiceBtn.classList.remove("listening"); };
}

let seededLocations = [];

async function loadSeededLocations() {
  const stateSelect = document.getElementById("stateSelect");
  if (!stateSelect) return;
  try {
    const response = await fetch(`${API_BASE_URL}/locations`);
    seededLocations = await response.json();

    const states = [...new Set(seededLocations.map(l => l.state).filter(Boolean))].sort();
    stateSelect.innerHTML = `<option value="">Select State</option>` +
      states.map(s => `<option value="${s}">${s}</option>`).join("");
  } catch (e) {
    stateSelect.innerHTML = `<option value="">Could not load — use manual entry below</option>`;
  }
}

function resetDependentSelects(fromLevel) {
  const districtSelect = document.getElementById("districtSelect");
  const blockSelect = document.getElementById("blockSelect");
  const villageSelect = document.getElementById("villageSelectSeed");

  if (["state", "district"].includes(fromLevel)) {
    districtSelect.innerHTML = `<option value="">Select state first</option>`;
    districtSelect.disabled = true;
  }
  if (["state", "district", "block"].includes(fromLevel)) {
    blockSelect.innerHTML = `<option value="">(no block data)</option>`;
    blockSelect.disabled = true;
  }
  villageSelect.innerHTML = `<option value="">Select district first</option>`;
  villageSelect.disabled = true;
  document.getElementById("locationIdInput").value = "";
}

function handleStateSelectChange() {
  const state = document.getElementById("stateSelect").value;
  resetDependentSelects("district");
  if (!state) return;

  const districts = [...new Set(
    seededLocations.filter(l => l.state === state).map(l => l.district).filter(Boolean)
  )].sort();

  const districtSelect = document.getElementById("districtSelect");
  districtSelect.innerHTML = `<option value="">Select District</option>` +
    districts.map(d => `<option value="${d}">${d}</option>`).join("");
  districtSelect.disabled = false;
}

function handleDistrictSelectChange() {
  const state = document.getElementById("stateSelect").value;
  const district = document.getElementById("districtSelect").value;
  resetDependentSelects("block");
  if (!district) return;

  const matches = seededLocations.filter(l => l.state === state && l.district === district);
  const blocks = [...new Set(matches.map(l => l.block).filter(Boolean))].sort();
  const blockSelect = document.getElementById("blockSelect");

  if (blocks.length > 0) {
    blockSelect.innerHTML = `<option value="">Select Block</option>` +
      blocks.map(b => `<option value="${b}">${b}</option>`).join("");
    blockSelect.disabled = false;
  } else {
    // no block-level data for this district -- skip straight to village
    blockSelect.innerHTML = `<option value="">(no block data for this district)</option>`;
    blockSelect.disabled = true;
    populateVillageSelect(matches);
  }
}

function handleBlockSelectChange() {
  const state = document.getElementById("stateSelect").value;
  const district = document.getElementById("districtSelect").value;
  const block = document.getElementById("blockSelect").value;

  const matches = seededLocations.filter(l =>
    l.state === state && l.district === district && (block ? l.block === block : true)
  );
  populateVillageSelect(matches);
}

function populateVillageSelect(matches) {
  const villageSelect = document.getElementById("villageSelectSeed");
  const sorted = [...matches].sort((a, b) => a.village_name.localeCompare(b.village_name));

  villageSelect.innerHTML = `<option value="">Select Village / City</option>` +
    sorted.map(l => `<option value="${l.id}">${l.village_name}</option>`).join("");
  villageSelect.disabled = false;
  document.getElementById("locationIdInput").value = "";
}

function handleVillageSelectSeedChange() {
  document.getElementById("locationIdInput").value = document.getElementById("villageSelectSeed").value || "";
}

function showManualLocationFallback() {
  document.getElementById("manualLocationGroup").style.display = "grid";
  document.getElementById("locationSelectGroup").style.display = "none";
  document.getElementById("unseededHint").style.display = "block";
  document.getElementById("locationIdInput").value = "";
}

function hideManualLocationFallback() {
  document.getElementById("manualLocationGroup").style.display = "none";
  document.getElementById("locationSelectGroup").style.display = "grid";
  document.getElementById("unseededHint").style.display = "none";
}

function getLocationFormValues() {
  const manualVisible = document.getElementById("manualLocationGroup").style.display !== "none";

  if (manualVisible) {
    return {
      state: document.getElementById("stateInput").value.trim(),
      district: document.getElementById("districtInput").value.trim(),
      location_id: null
    };
  }

  const stateSel = document.getElementById("stateSelect");
  const districtSel = document.getElementById("districtSelect");
  const villageSel = document.getElementById("villageSelectSeed");

  return {
    state: stateSel ? stateSel.value : "",
    district: districtSel ? districtSel.value : "",
    location_id: villageSel && villageSel.value ? parseInt(villageSel.value, 10) : null
  };
}

function formatMarkdownToHTML(text) {

  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return escaped
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")  
    .replace(/\n/g, "<br>");                            
}

function appendChatBubble(text, sender) {
  const history = document.getElementById("chatHistory");
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = formatMarkdownToHTML(text);
  history.appendChild(bubble);
  history.scrollTop = history.scrollHeight;
}

// Wizard Submission Handler
async function submitWizardToFastAPI() {
  const marginInput = document.getElementById("marginInput");
  const categorySelect = document.getElementById("categorySelect");

  const marginCapital = parseFloat(marginInput ? marginInput.value : 0);
  const category = categorySelect ? categorySelect.value : "dairy";

  if (!marginCapital) return alert("Please enter a valid margin capital amount.");

  const loc = getLocationFormValues();

  const payload = {
    state: loc.state || "Maharashtra",
    district: loc.district || null,
    business_category: category,
    margin_pct: 0.10,
    margin_capital: marginCapital,
    experience_level: "beginner",
    location_id: loc.location_id
  };

  await fetchAndRenderResult("/feasibility", payload);
}

// Chat AI Submission Handler
async function submitChatToFastAPI() {
  const inputEl = document.getElementById("chatInput");
  if (!inputEl) return;
  const message = inputEl.value.trim();
  if (!message) return;

  inputEl.value = "";
  appendChatBubble(message, "user");

  const payload = {
    message: message,
    experience_level: "beginner"
  };

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("API Error");
    const data = await response.json();
    
    appendChatBubble(data.explanation || "I have analyzed your request. See the report below!", "ai");
    renderReport(data);

  } catch (err) {
    appendChatBubble(t('errorServer'), "ai");
  }
}

async function fetchAndRenderResult(endpoint, payload) {
  const resultSec = document.getElementById("resultSection");
  const loader = document.getElementById("loadingIndicator");
  
  if (resultSec) resultSec.hidden = false;
  if (loader) loader.hidden = false;
  document.getElementById("resultContent").innerHTML = "";
  if (resultSec) resultSec.scrollIntoView({ behavior: "smooth" });

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Server error");
    }

    const data = await response.json();
    if (loader) loader.hidden = true;
    renderReport(data);

  } catch (err) {
    if (loader) loader.hidden = true;
    document.getElementById("resultContent").innerHTML = `<p style="color:red">Error: ${err.message}</p>`;
  }
}

function renderReport(data) {
  const content = document.getElementById("resultContent");
  if (!content) return;
  
  const schemeName = data.scheme?.name || "Standard Loan";
  const projectCost = data.loan?.project_cost || 0;
  const marginMoney = data.loan?.margin_amount || 0;
  const loanAmount = data.loan?.loan_amount || 0;
  const emi = data.installment || 0;
  
  let swotHTML = "";
  if (data.swot) {
    let swotContent = typeof data.swot === 'string' ? data.swot.replace(/\n/g, '<br>') : `
      <p><strong>Strengths:</strong> ${data.swot.strengths || 'N/A'}</p>
      <p><strong>Weaknesses:</strong> ${data.swot.weaknesses || 'N/A'}</p>
      <p><strong>Opportunities:</strong> ${data.swot.opportunities || 'N/A'}</p>
      <p><strong>Threats:</strong> ${data.swot.threats || 'N/A'}</p>
    `;
    
    swotHTML = `
    <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 20px 0;">
    <h3 style="margin-top:0">AI Market Analysis (SWOT)</h3>
    ${swotContent}
    `;
  }

  let competitorHTML = "";
  if (data.competitor_mapping && data.competitor_mapping.nearest && data.competitor_mapping.nearest.length > 0) {
    competitorHTML = `
    <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 20px 0;">
    <h3 style="margin-top:0">Nearby Competitors (Live OSM Data)</h3>
    <div id="competitorMapDiv" style="height: 250px; width: 100%; margin-bottom: 15px; border-radius: 8px;"></div>
    <ul class="competitor-list" style="list-style: none; padding: 0;">
      ${data.competitor_mapping.nearest.slice(0, 5).map(comp => `
        <li class="competitor-card" style="padding: 8px; border-bottom: 1px solid #E2E8F0; display: flex; justify-content: space-between;">
          <span class="competitor-name">${comp.name || 'Unnamed Business'}</span>
          <span class="competitor-dist" style="color: #64748B;">${comp.distance_km} km away</span>
        </li>
      `).join('')}
    </ul>
    `;
  } else if (data.competitor_mapping && data.competitor_mapping.nearest && data.competitor_mapping.nearest.length === 0) {
    competitorHTML = `<p><em>No immediate competitors found in the OpenStreetMap database for this radius.</em></p>`;
  }

  content.innerHTML = `
    <div class="step-card" style="border-left: 4px solid var(--primary, #0D9488);">
      <h3 style="margin-top:0">Selected Scheme: ${schemeName}</h3>
      <p><strong>Total Project Cost:</strong> ₹${projectCost.toLocaleString('en-IN')}</p>
      <p><strong>Your Contribution (Margin):</strong> ₹${marginMoney.toLocaleString('en-IN')}</p>
      <p><strong>Loan Amount (90%):</strong> ₹${loanAmount.toLocaleString('en-IN')}</p>
      <p><strong>Estimated Repayment:</strong> ₹${emi.toLocaleString('en-IN')} per installment</p>
      ${swotHTML}
      ${competitorHTML}
    </div>
  `;

  if (data.competitor_mapping && data.competitor_mapping.nearest && data.competitor_mapping.nearest.length > 0) {
    renderCompetitorMap(data.competitor_mapping.nearest);
  }
}

// Business Journal Handlers
async function submitJournalEntry() {
  const date = document.getElementById("journalDate").value;
  const sales = parseFloat(document.getElementById("journalSales").value) || 0;
  const expenses = parseFloat(document.getElementById("journalExpenses").value) || 0;
  const units = parseFloat(document.getElementById("journalUnits").value) || 0;

  if (!date) return alert("Please select a date.");

  const payload = { entry_date: date, sales_revenue: sales, expenses: expenses, units_sold: units };

  try {
    const response = await fetch(`${API_BASE_URL}/journal/entry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (response.ok) {
      const statusText = document.getElementById("journalLogStatus");
      if (statusText) {
        statusText.style.display = "block";
        setTimeout(() => statusText.style.display = "none", 3000);
      }
      document.getElementById("journalSales").value = "";
      document.getElementById("journalExpenses").value = "";
      document.getElementById("journalUnits").value = "";
      fetchJournalEntries();
    }
  } catch (e) {
    alert("Failed to save entry.");
  }
}

async function askJournal() {
  const queryEl = document.getElementById("journalQuery");
  const answerDiv = document.getElementById("journalAnswer");
  
  if (!queryEl || !answerDiv) return;
  const query = queryEl.value;
  
  if (!query) return;
  answerDiv.innerHTML = "<em>Analyzing your ledger...</em>";

  try {
    const response = await fetch(`${API_BASE_URL}/journal/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: query })
    });
    
    const data = await response.json();
    
    if (data.error) {
      answerDiv.innerHTML = `<span style="color:red">${data.error}</span>`;
    } else if (data.intent === "summary") {
      answerDiv.innerHTML = `Total Sales: ₹${data.result.total_sales || 0} | Total Expenses: ₹${data.result.total_expenses || 0}`;
    } else if (data.intent === "max" || data.intent === "min") {
      const val = data.result[data.field];
      answerDiv.innerHTML = `The ${data.intent} ${data.field} was <strong>₹${val}</strong> on ${data.result.entry_date}.`;
    } else {
      answerDiv.innerHTML = `Query processed successfully.`;
    }
  } catch (e) {
    answerDiv.innerHTML = `<span style="color:red">Failed to reach the AI.</span>`;
  }
}

async function fetchJournalEntries() {
  const tbody = document.getElementById("journalTableBody");
  if (!tbody) return;

  tbody.innerHTML = `<tr><td colspan="4" style="padding: 12px; text-align: center;">Loading entries...</td></tr>`;

  try {
    const response = await fetch(`${API_BASE_URL}/journal/entries`);
    const entries = await response.json();

    if (!entries || entries.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" style="padding: 12px; text-align: center; color: #64748B;">No journal entries found. Log one above!</td></tr>`;
      return;
    }

    tbody.innerHTML = entries.map(entry => `
      <tr style="border-bottom: 1px solid #E2E8F0;">
        <td style="padding: 8px;">${entry.entry_date}</td>
        <td style="padding: 8px; color: #10B981;">₹${entry.sales_revenue || 0}</td>
        <td style="padding: 8px; color: #EF4444;">₹${entry.expenses || 0}</td>
        <td style="padding: 8px;">${entry.units_sold || '-'}</td>
      </tr>
    `).join('');
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" style="padding: 12px; text-align: center; color: red;">Failed to load journal records.</td></tr>`;
  }
}

// Dynamic Read-Aloud (Text-to-Speech) Functionality
function readReportAloud() {
  const content = document.getElementById("resultContent")?.innerText;
  if (!content) return alert("No report to read yet!");

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(content);
  utterance.lang = langVoiceMap[currentLang] || 'en-IN';
  utterance.rate = 0.9;
  
  window.speechSynthesis.speak(utterance);
}

// Leaflet Map Renderer for Nearby Competitors
let competitorMap = null;

function renderCompetitorMap(competitors) {
  const mapContainerId = "competitorMapDiv";
  let mapDiv = document.getElementById(mapContainerId);
  
  if (!mapDiv || typeof L === "undefined") return;

  if (competitorMap) {
    competitorMap.remove();
    competitorMap = null;
  }

  const defaultLat = 20.5937; 
  const defaultLon = 78.9629;

  competitorMap = L.map(mapContainerId).setView([defaultLat, defaultLon], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(competitorMap);

  if (competitors && competitors.length > 0) {
    const bounds = [];
    competitors.forEach((comp, index) => {
      const lat = comp.lat || (defaultLat + (index * 0.01));
      const lon = comp.lon || (defaultLon + (index * 0.01));
      
      const marker = L.marker([lat, lon]).addTo(competitorMap);
      marker.bindPopup(`<b>${comp.name || 'Competitor'}</b><br>${comp.distance_km} km away`);
      bounds.push([lat, lon]);
    });

    if (bounds.length > 0) {
      competitorMap.fitBounds(bounds, { padding: [30, 30] });
    }
  }
}