export const rules = {
  required: (v: any) => !!v || 'Обязательное поле',

  positive: (v: any) => {
    if (v === null || v === undefined || v === '') return true;
    return Number(v) >= 0 || 'Число должно быть положительным';
  },

  email: (v: string) => {
    if (!v) return true;
    const pattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return pattern.test(v) || 'Некорректный формат E-mail';
  },

  nickname: (v: string) => {
    if (!v) return true;
    const pattern = /^[a-zA-Z0-9_]+$/;
    return pattern.test(v) || 'Только буквы, цифры и нижнее подчеркивание';
  },
};

export const blockInvalidNumberChars = (e: KeyboardEvent) => {
  if (['-', '+', 'e', 'E'].includes(e.key)) {
    e.preventDefault();
  }
};
