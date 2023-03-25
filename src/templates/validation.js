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
  fund: errMsgTextInput,             
  email: {
    required: "Пожалуйста, укажите адрес электронной почты, допустимые символы [a-z 0-9 _ @ .]",
    min: "Введите не менее 5 символов",
    max: "Достигнут максимально разрешенный размер поля ввода",
  },
  phone_number: {
    required: "Введите 10-значный телефонный номер (без +7 или 8, например 921345хххх)",
    min: "Вы ввели менее 10 цифр, продолжайте ввод номера",
    max: "Вы ввели более 10 цифр, откорретируйте ввод номера",
  },
};
  
// VALIDATION 
const setValid = (element, errElement) => {
    element.classList.remove("invalid");
    errElement.textContent = "";
};
  
const setInvalid = (element, errElement, errName) => {
    element.classList.add("invalid");
    errElement.textContent = errMsg[element.name][errName];
};

const checkInputValidity = (
  element,
  errElement,
) => {
  const minlength = element.getAttribute("minlength");
  const maxlength = element.getAttribute("maximumlength");
  const capsPattern = /[А-ЯЁ]{2,}/g;
  let newValue = element.value;
  
  if (element.name == 'email') {
    not_allowed_simbols = /[^a-z0-9_@\.]/;
    isCapitalize = false;
  }
  else if (element.name == "phone_number") {
    not_allowed_simbols = /[^0-9]/;
    isCapitalize = false;
  }  
  else {
    not_allowed_simbols = /[^А-Яа-я]/;
    isCapitalize = true;
  }
  newValue = newValue.trimStart().replace(not_allowed_simbols, "");
  
  if (isCapitalize && newValue) {
    newValue = newValue
      .split("-")
      .map((word) => (
        word ? word.replace(
          /^(?!на)[а-яё]{2}/, letter => letter[0].toUpperCase() + letter.slice(1)
        ) : "")
      )
      .join("-")
      .split(" ")
      .map((word) => (word ? word[0].toUpperCase() + word.slice(1) : ""))
      .join(" ");
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

const showTgButton = (tgMainButton) => {
  tgMainButton.setText("Зарегистрироваться в проекте");
  tgMainButton.show();
};

// send data to server
const handleSubmit = (inputs, tg) => {
  tg.MainButton.disable();

  const data = Array.from(inputs).reduce((data, input) => {
    data[input.name] = input.value.trim();
    return data;
  }, {});

  tg.sendData(JSON.stringify(data));
  tg.close();
};

// content loaded, main actions
document.addEventListener("DOMContentLoaded", function () {
  const tg = window.Telegram.WebApp;
  tg.ready();
  tg.expand();

  const tgMainButton = tg.MainButton;
  const defaultButtonColor = tg.themeParams.button_color;
  const defaultButtonTextColor = tg.themeParams.button_text_color;

  const inputElements = document.querySelectorAll(".validate");

  setValidation(
    inputElements,
    tgMainButton,
    defaultButtonColor,
    defaultButtonTextColor
  );
  tgMainButton.onClick(() => handleSubmit(inputElements, tg));
  showTgButton(tgMainButton);
}
);