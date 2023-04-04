// === ENTRYPOINT ===
const inputElements = document.querySelectorAll(".validate");
const fund = document.getElementById("fund");
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();
tg.MainButton.setText("Оформить заявку").show();
if (!fund.required) {
  tg.BackButton.show();
}

// === VALIDATION ===
const errMsgTextInput = {
  required: "Поле обязательно для заполнения на кириллице",
  min: "Пожалуйста, заполните поле на кириллице (не менее 2 символов)",
  max: "Допускается ввод не более 100 символов",
  capsPattern: "Убедитесь, что у Вас выключен CAPS LOCK",
};
  
const errMsg = {
  surname: errMsgTextInput,    
  name: errMsgTextInput,
  patronimic: errMsgTextInput,      
  occupation: errMsgTextInput,
  location: errMsgTextInput,   
  fund: {
    required: "Пожалуйста, укажите название фонда, допускаются любые буквы, цифры и знак пробела",
    min: "Введите не менее 2 символов",
    max: "Допускается ввод не более 100 символов",
  },             
  email: {
    required: "Пожалуйста, укажите адрес электронной почты, допустимые символы [a-z 0-9 _ @ .]",
    min: "Введите не менее 5 символов",
    max: "Достигнут максимально разрешенный размер поля ввода",
  },
  phone_number: {
    required: "Введите 10-значный телефонный номер (без +7 или 8, например 921345хххх)",
    min: "Вы ввели менее 10 цифр, продолжайте ввод номера",
    max: "Вы ввели более 10 цифр, откорректируйте ввод номера",
  },
};
  
const setValid = (element, errElement) => {
    element.classList.remove("invalid");
    errElement.textContent = "";
};
  
const setInvalid = (element, errElement, errName) => {
    element.classList.add("invalid");
    errElement.textContent = errMsg[element.name][errName];
};

const checkInputValidity = (element, errElement) => {
  const minlength = element.getAttribute("minlength");
  const maxlength = element.getAttribute("maximumlength");
  const capsPattern = /[А-ЯЁ]{2,}/;
  let newValue = element.value;

  switch (element.name) { 
   case "email":
    not_allowed_simbols = /[^a-z0-9_@\.]/;
    isCapitalize = false;
    break;
   case "phone_number":
    not_allowed_simbols = /[^0-9]/;
    isCapitalize = false;
    break;
   case "fund":
    not_allowed_simbols = /[^А-Яа-я\w\s]/
    isCapitalize = false;
    break;
   default:
    not_allowed_simbols = /[^А-Яа-я]/;
    isCapitalize = true;    
  } 
  
  if (not_allowed_simbols) {
    newValue = newValue.trimStart().replace(not_allowed_simbols, "");
  }
  
    
  if (!newValue) {
    setInvalid(element, errElement, "required");
  } 
  else if (element.name == "phone_number" && newValue[0] != "8") {
    newValue = "8" + newValue;
  }
  else if (minlength && newValue.length < minlength) {
    setInvalid(element, errElement, "min");
  } 
  else if (maxlength && newValue.length > maxlength) {
    setInvalid(element, errElement, "max");
  } 
  else if (newValue.match(capsPattern)) {
    setInvalid(element, errElement, "capsPattern");
  }
  else if (element.name == "email" && !newValue.match(/^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/)) {
    setInvalid(element, errElement, "required");
  } 
  else {
    if (isCapitalize && ![/[А-Я]/].includes(newValue[0])) {
      newValue = newValue[0].toUpperCase() + newValue.slice(1)
    }
    setValid(element, errElement);
  }
  element.value = newValue;
};

const toggleSubmitState = (
  inputs,
  tgMainButton,
  defaultButtonColor,
  defaultButtonTextColor
) => {
  const isValidationError = Array.from(inputs).some(
    (input) =>
      !input.validity.valid || input.classList.contains("invalid")
  );
  if (isValidationError) {
    tgMainButton.setParams({
      is_active: false,
      color: "#9e9e9e",
      text_color: "#eceff1",
    });
  } else {
    tgMainButton.setParams({
      is_active: true,
      color: defaultButtonColor,
      text_color: defaultButtonTextColor,
    });
  }
};

const setValidation = (
  inputs,
  tgMainButton,
  defaultButtonColor,
  defaultButtonTextColor
) => {
  toggleSubmitState(
    inputs,
    tgMainButton,
    defaultButtonColor,
    defaultButtonTextColor
  );

  inputs.forEach((input) => {
    const errElement = document.querySelector(
      `.helper-text.${input.name}`
    );

    const check = () => {
      checkInputValidity(input, errElement)
      toggleSubmitState(
        inputs,
        tgMainButton,
        defaultButtonColor,
        defaultButtonTextColor
      );
    };

    input.oninput = () => check();
    input.onblur = () => check();
    input.onchange = () => check();
    input.onpaste = () => check();
  });
};


setValidation(
  inputElements,
  tg.MainButton,
  tg.themeParams.button_color,
  tg.themeParams.button_text_color
);


// === SENDING DATA ===
const handleSubmit = (inputs, tg) => {
  tg.MainButton.disable();
  const data = Array.from(inputs).reduce((data, input) => {
    data[input.name] = input.value.trim();
    return data;
  }, {}); 
  tg.sendData(JSON.stringify(data));
  tg.close();
};

const handleBack = (tg) => {
  tg.sendData(JSON.stringify({back: "get_fund"}));
  tg.close();
};

tg.BackButton.onClick(() => handleBack(tg));
tg.MainButton.onClick(() => handleSubmit(inputElements, tg));

