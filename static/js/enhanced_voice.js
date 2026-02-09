// Enhanced Voice Assistant for Multilingual Healthcare System

class VoiceAssistant {
    constructor(language = 'en') {
        this.language = language;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.currentField = null;
        this.voices = [];
        
        this.initializeVoiceRecognition();
        this.initializeVoiceSynthesis();
        this.setupEventListeners();
    }
    
    initializeVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = this.getLanguageCode();
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.updateVoiceStatus('listening');
                this.highlightActiveField();
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.processVoiceInput(transcript);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                this.updateVoiceStatus('ready');
                this.removeFieldHighlight();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceStatus('error');
                this.speakText(this.getTranslation('voice_error'));
            };
        }
    }
    
    initializeVoiceSynthesis() {
        if (this.synthesis) {
            // Wait for voices to load
            const loadVoices = () => {
                this.voices = this.synthesis.getVoices();
                this.selectBestVoice();
            };
            
            loadVoices();
            this.synthesis.onvoiceschanged = loadVoices;
        }
    }
    
    selectBestVoice() {
        const languageCode = this.getLanguageCode();
        const preferredVoices = this.voices.filter(voice => 
            voice.lang.startsWith(languageCode.split('-')[0])
        );
        
        // Prefer female voices for healthcare applications (generally perceived as more caring)
        const femaleVoices = preferredVoices.filter(voice => 
            voice.name.toLowerCase().includes('female') || 
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('zira') ||
            voice.name.toLowerCase().includes('susan')
        );
        
        this.selectedVoice = femaleVoices[0] || preferredVoices[0] || this.voices[0];
    }
    
    getLanguageCode() {
        const languageCodes = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'ta': 'ta-IN'
        };
        return languageCodes[this.language] || 'en-US';
    }
    
    getTranslation(key) {
        const translations = {
            'en': {
                'listening': 'Listening...',
                'ready': 'Voice assistant ready',
                'error': 'Voice recognition error',
                'voice_error': 'Sorry, I could not understand. Please try again.',
                'field_filled': 'Field filled',
                'next_field': 'Moving to next field',
                'form_complete': 'Form completed',
                'welcome': 'Welcome to patient registration. I will help you fill out the form.',
                'name_prompt': 'Please say your full name',
                'age_prompt': 'Please say your age',
                'symptom_prompt': 'Please describe your symptoms',
                'severity_mild': 'Mild severity selected',
                'severity_moderate': 'Moderate severity selected',
                'severity_severe': 'Severe severity selected',
                'emergency_on': 'Emergency mode activated',
                'emergency_off': 'Emergency mode deactivated'
            },
            'hi': {
                'listening': 'सुन रहा है...',
                'ready': 'आवाज सहायक तैयार है',
                'error': 'आवाज पहचान त्रुटि',
                'voice_error': 'माफ करें, मैं समझ नहीं सका। कृपया फिर से कोशिश करें।',
                'field_filled': 'फील्ड भरा गया',
                'next_field': 'अगले फील्ड पर जा रहे हैं',
                'form_complete': 'फॉर्म पूरा हुआ',
                'welcome': 'रोगी पंजीकरण में आपका स्वागत है। मैं फॉर्म भरने में आपकी मदद करूंगा।',
                'name_prompt': 'कृपया अपना पूरा नाम बताएं',
                'age_prompt': 'कृपया अपनी उम्र बताएं',
                'symptom_prompt': 'कृपया अपने लक्षणों का वर्णन करें',
                'severity_mild': 'हल्की गंभीरता चुनी गई',
                'severity_moderate': 'मध्यम गंभीरता चुनी गई',
                'severity_severe': 'गंभीर गंभीरता चुनी गई',
                'emergency_on': 'आपातकालीन मोड सक्रिय',
                'emergency_off': 'आपातकालीन मोड निष्क्रिय'
            },
            'ta': {
                'listening': 'கேட்கிறது...',
                'ready': 'குரல் உதவியாளர் தயார்',
                'error': 'குரல் அங்கீகார பிழை',
                'voice_error': 'மன்னிக்கவும், என்னால் புரிந்து கொள்ள முடியவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.',
                'field_filled': 'புலம் நிரப்பப்பட்டது',
                'next_field': 'அடுத்த புலத்திற்கு செல்கிறது',
                'form_complete': 'படிவம் முடிந்தது',
                'welcome': 'நோயாளி பதிவுக்கு வரவேற்கிறோம். படிவத்தை நிரப்ப நான் உங்களுக்கு உதவுவேன்.',
                'name_prompt': 'தயவுசெய்து உங்கள் முழு பெயரைச் சொல்லுங்கள்',
                'age_prompt': 'தயவுசெய்து உங்கள் வயதைச் சொல்லுங்கள்',
                'symptom_prompt': 'தயவுசெய்து உங்கள் அறிகுறிகளை விவரிக்கவும்',
                'severity_mild': 'லேசான தீவிரம் தேர்ந்தெடுக்கப்பட்டது',
                'severity_moderate': 'மிதமான தீவிரம் தேர்ந்தெடுக்கப்பட்டது',
                'severity_severe': 'கடுமையான தீவிரம் தேர்ந்தெடுக்கப்பட்டது',
                'emergency_on': 'அவசர பயன்முறை செயல்படுத்தப்பட்டது',
                'emergency_off': 'அவசர பயன்முறை செயலிழக்கப்பட்டது'
            }
        };
        
        return translations[this.language]?.[key] || translations['en'][key] || key;
    }
    
    setupEventListeners() {
        // Voice control buttons
        const startBtn = document.getElementById('startVoiceBtn');
        const stopBtn = document.getElementById('stopVoiceBtn');
        const repeatBtn = document.getElementById('repeatBtn');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startListening());
        }
        
        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopListening());
        }
        
        if (repeatBtn) {
            repeatBtn.addEventListener('click', () => this.repeatInstructions());
        }
        
        // Form field focus listeners
        this.setupFormFieldListeners();
    }
    
    setupFormFieldListeners() {
        const formFields = document.querySelectorAll('input, select, textarea');
        formFields.forEach(field => {
            field.addEventListener('focus', (e) => {
                this.currentField = e.target;
                this.announceFieldFocus(e.target);
            });
        });
    }
    
    announceFieldFocus(field) {
        const label = this.getFieldLabel(field);
        if (label) {
            this.speakText(`Now entering ${label}`);
        }
    }
    
    getFieldLabel(field) {
        const label = field.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            return label.textContent.replace('*', '').trim();
        }
        return field.placeholder || field.name || 'field';
    }
    
    startListening() {
        if (this.recognition && !this.isListening) {
            this.recognition.start();
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
    
    speakText(text, options = {}) {
        if (this.synthesis && text) {
            // Cancel any ongoing speech
            this.synthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.getLanguageCode();
            utterance.rate = options.rate || 0.8;
            utterance.pitch = options.pitch || 1;
            utterance.volume = options.volume || 1;
            
            if (this.selectedVoice) {
                utterance.voice = this.selectedVoice;
            }
            
            this.synthesis.speak(utterance);
        }
    }
    
    processVoiceInput(transcript) {
        console.log('Voice input:', transcript);
        
        const lowerTranscript = transcript.toLowerCase();
        
        // Command processing
        if (this.isCommand(lowerTranscript)) {
            this.processCommand(lowerTranscript);
            return;
        }
        
        // Field-specific processing
        if (this.currentField) {
            this.fillCurrentField(transcript);
        } else {
            this.processGeneralInput(transcript);
        }
    }
    
    isCommand(transcript) {
        const commands = [
            'next field', 'next', 'अगला', 'அடுத்து',
            'previous field', 'previous', 'पिछला', 'முந்தைய',
            'repeat', 'दोहराएं', 'மீண்டும்',
            'help', 'मदद', 'உதவி',
            'emergency', 'आपातकाल', 'அவசர',
            'mild', 'moderate', 'severe',
            'हल्का', 'मध्यम', 'गंभीर',
            'லேசான', 'மிதமான', 'கடுமையான'
        ];
        
        return commands.some(cmd => transcript.includes(cmd));
    }
    
    processCommand(transcript) {
        // Navigation commands
        if (transcript.includes('next') || transcript.includes('अगला') || transcript.includes('அடுத்து')) {
            this.moveToNextField();
        } else if (transcript.includes('previous') || transcript.includes('पिछला') || transcript.includes('முந்தைய')) {
            this.moveToPreviousField();
        }
        
        // Severity commands
        else if (transcript.includes('mild') || transcript.includes('हल्का') || transcript.includes('லேசான')) {
            this.selectSeverity('Mild');
        } else if (transcript.includes('moderate') || transcript.includes('मध्यम') || transcript.includes('மிதமான')) {
            this.selectSeverity('Moderate');
        } else if (transcript.includes('severe') || transcript.includes('गंभीर') || transcript.includes('கடுமையான')) {
            this.selectSeverity('Severe');
        }
        
        // Emergency command
        else if (transcript.includes('emergency') || transcript.includes('आपातकाल') || transcript.includes('அவசர')) {
            this.toggleEmergency();
        }
        
        // Help command
        else if (transcript.includes('help') || transcript.includes('मदद') || transcript.includes('உதவி')) {
            this.provideHelp();
        }
        
        // Repeat command
        else if (transcript.includes('repeat') || transcript.includes('दोहराएं') || transcript.includes('மீண்டும்')) {
            this.repeatInstructions();
        }
    }
    
    fillCurrentField(transcript) {
        if (!this.currentField) return;
        
        const fieldType = this.currentField.type || this.currentField.tagName.toLowerCase();
        
        switch (fieldType) {
            case 'text':
            case 'tel':
            case 'email':
            case 'textarea':
                this.currentField.value = transcript;
                this.speakText(this.getTranslation('field_filled'));
                break;
                
            case 'number':
                const number = this.extractNumber(transcript);
                if (number) {
                    this.currentField.value = number;
                    this.speakText(this.getTranslation('field_filled'));
                }
                break;
                
            case 'select':
                this.selectOption(transcript);
                break;
        }
        
        // Auto-move to next field after filling
        setTimeout(() => {
            this.moveToNextField();
        }, 1000);
    }
    
    extractNumber(transcript) {
        const numbers = transcript.match(/\d+/);
        return numbers ? numbers[0] : null;
    }
    
    selectOption(transcript) {
        const select = this.currentField;
        const options = Array.from(select.options);
        
        // Try to match transcript with option text
        const matchedOption = options.find(option => 
            option.text.toLowerCase().includes(transcript.toLowerCase()) ||
            transcript.toLowerCase().includes(option.text.toLowerCase())
        );
        
        if (matchedOption) {
            select.value = matchedOption.value;
            this.speakText(`${matchedOption.text} selected`);
        }
    }
    
    selectSeverity(severity) {
        const severityBtn = document.querySelector(`.severity-btn.${severity.toLowerCase()}`);
        if (severityBtn && window.selectSeverity) {
            window.selectSeverity(severity, severityBtn);
            this.speakText(this.getTranslation(`severity_${severity.toLowerCase()}`));
        }
    }
    
    toggleEmergency() {
        const emergencySwitch = document.getElementById('emergencySwitch');
        if (emergencySwitch && window.toggleEmergency) {
            window.toggleEmergency();
            const isActive = emergencySwitch.classList.contains('active');
            this.speakText(this.getTranslation(isActive ? 'emergency_on' : 'emergency_off'));
        }
    }
    
    moveToNextField() {
        const formFields = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
        const currentIndex = formFields.indexOf(this.currentField);
        
        if (currentIndex < formFields.length - 1) {
            const nextField = formFields[currentIndex + 1];
            nextField.focus();
            this.speakText(this.getTranslation('next_field'));
        } else {
            this.speakText(this.getTranslation('form_complete'));
        }
    }
    
    moveToPreviousField() {
        const formFields = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'));
        const currentIndex = formFields.indexOf(this.currentField);
        
        if (currentIndex > 0) {
            const previousField = formFields[currentIndex - 1];
            previousField.focus();
            this.speakText('Previous field');
        }
    }
    
    processGeneralInput(transcript) {
        // Try to identify what the user is trying to fill
        const lowerTranscript = transcript.toLowerCase();
        
        // Name detection
        if (lowerTranscript.includes('name is') || lowerTranscript.includes('नाम है') || lowerTranscript.includes('பெயர்')) {
            const nameField = document.getElementById('name');
            if (nameField) {
                const nameMatch = transcript.match(/(?:name is|नाम है|பெயர்)\s*(.+)/i);
                if (nameMatch) {
                    nameField.value = nameMatch[1].trim();
                    nameField.focus();
                    this.speakText('Name recorded');
                }
            }
        }
        
        // Age detection
        else if (lowerTranscript.includes('age') || lowerTranscript.includes('उम्र') || lowerTranscript.includes('வயது')) {
            const ageField = document.getElementById('age');
            if (ageField) {
                const ageMatch = transcript.match(/\d+/);
                if (ageMatch) {
                    ageField.value = ageMatch[0];
                    ageField.focus();
                    this.speakText('Age recorded');
                }
            }
        }
        
        // Symptom detection
        else if (lowerTranscript.includes('symptom') || lowerTranscript.includes('लक्षण') || lowerTranscript.includes('அறிகுறி')) {
            const symptomField = document.getElementById('main_symptom');
            if (symptomField) {
                symptomField.value = transcript;
                symptomField.focus();
                this.speakText('Symptoms recorded');
            }
        }
    }
    
    provideHelp() {
        const helpText = `You can say commands like: "My name is John", "Age 25", "Next field", "Emergency", "Mild severity", or describe your symptoms directly.`;
        this.speakText(helpText);
    }
    
    repeatInstructions() {
        const instructions = this.getTranslation('welcome');
        this.speakText(instructions);
    }
    
    updateVoiceStatus(status) {
        const statusElement = document.getElementById('voiceStatus');
        if (statusElement) {
            statusElement.textContent = this.getTranslation(status);
            
            // Update button states
            const startBtn = document.getElementById('startVoiceBtn');
            const stopBtn = document.getElementById('stopVoiceBtn');
            
            if (startBtn && stopBtn) {
                if (status === 'listening') {
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                } else {
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                }
            }
        }
    }
    
    highlightActiveField() {
        if (this.currentField) {
            this.currentField.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.3)';
            this.currentField.style.borderColor = '#4caf50';
        }
    }
    
    removeFieldHighlight() {
        if (this.currentField) {
            this.currentField.style.boxShadow = '';
            this.currentField.style.borderColor = '';
        }
    }
    
    // Public methods for external use
    setLanguage(language) {
        this.language = language;
        if (this.recognition) {
            this.recognition.lang = this.getLanguageCode();
        }
        this.selectBestVoice();
    }
    
    announcePageContent(content) {
        setTimeout(() => {
            this.speakText(content);
        }, 1000);
    }
    
    announceFormCompletion(registrationId, department) {
        const message = `Registration successful. Your ID is ${registrationId}. Department: ${department}`;
        this.speakText(message);
    }
    
    announceStatusUpdate(status, patientName) {
        const message = `Status update for ${patientName}: ${status}`;
        this.speakText(message);
    }
}

// Global voice assistant instance
let voiceAssistant = null;

// Initialize voice assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get language from URL or session
    const urlParams = new URLSearchParams(window.location.search);
    const language = urlParams.get('lang') || 
                    document.documentElement.lang || 
                    'en';
    
    // Initialize voice assistant
    voiceAssistant = new VoiceAssistant(language);
    
    // Announce page content for accessibility
    const pageTitle = document.title;
    if (pageTitle.includes('Registration') || pageTitle.includes('पंजीकरण') || pageTitle.includes('பதிவு')) {
        voiceAssistant.announcePageContent(voiceAssistant.getTranslation('welcome'));
    }
});

// Export for use in other scripts
window.VoiceAssistant = VoiceAssistant;
window.voiceAssistant = voiceAssistant;