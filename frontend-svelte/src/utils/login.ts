import { navigate } from "svelte-routing";
import { getCookie } from '../utils/cookie';
import { isAuthenticated } from "../stores/isAuthenticatedStore";
import { isLoginModalOpen } from "../stores/isLoginModalOpenStore";

let csrfToken: string | any;

csrfToken = getCookie('csrftoken');

let loginMessage: string | any = '';

export async function login(username: string, password: string) {
    try {

      const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();

      if (response.ok) {
        isAuthenticated.set(data.is_authenticated);
        navigate("/app/dashboard", { replace: true });
        isLoginModalOpen.set(false); // Close the modal on successful login
        loginMessage = 'Login successful'
        return loginMessage
      } else {
        // Handle login error
        throw new Error(data.message);
      }

    } catch (error) {
      console.error('Login unsuccessful in catch:', error);
      loginMessage = (error as Error).message;
      throw error;
    }
  }