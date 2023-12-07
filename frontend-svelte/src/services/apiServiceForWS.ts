export const createWorkspace = async (formData: FormData): Promise<any> => {
    try {
      const response = await fetch('http://localhost:8000/api/create_workspace/', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      return await response.json();
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      throw new Error('Failed to create workspace');
    }
  };