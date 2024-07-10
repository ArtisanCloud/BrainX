const token_key = 'token';

const isLogin = () => {
	return !!sessionStorage.getItem(token_key);
};

const getToken = () => {
	return sessionStorage.getItem(token_key);
};

const setToken = (token: string) => {
	sessionStorage.setItem(token_key, token);
};

const clearToken = () => {
	sessionStorage.removeItem(token_key);
};

export { isLogin, getToken, setToken, clearToken };
