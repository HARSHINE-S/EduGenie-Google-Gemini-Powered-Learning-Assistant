function buildPayload(endpoint, value) {
  switch (endpoint) {
    case '/api/qna':
      return { question: value };
    case '/api/explain':
      return { topic: value, level: 'beginner' };
    case '/api/summarize':
      return { text: value, focus: 'main idea' };
    case '/api/quiz':
      return { topic: value, num_questions: 3 };
    case '/api/learning-path':
      return { subject: value, student_level: 'beginner' };
    case '/api/recommendations':
      return { subject: value, student_level: 'beginner' };
    default:
      return { input: value };
  }
}

function formatResult(data) {
  if (!data || typeof data !== 'object') {
    return String(data ?? 'No response received.');
  }

  if (typeof data.answer === 'string') return data.answer;
  if (typeof data.explanation === 'string') return data.explanation;
  if (typeof data.summary === 'string') return data.summary;
  if (typeof data.message === 'string') return data.message;

  if (Array.isArray(data.steps)) {
    const subject = data.subject ? `Learning path for ${data.subject}:` : 'Learning path:';
    const items = data.steps.map((step, index) => `${index + 1}. ${step}`).join('\n');
    return `${subject}\n${items}`;
  }

  if (Array.isArray(data.recommendations)) {
    const subject = data.subject ? `Recommended study actions for ${data.subject}:` : 'Recommended study actions:';
    const items = data.recommendations.map((item, index) => `${index + 1}. ${item}`).join('\n');
    return `${subject}\n${items}`;
  }

  if (Array.isArray(data.questions)) {
    return data.questions
      .map((item, index) => {
        const options = item.options ? item.options.map((option, optionIndex) => `  ${String.fromCharCode(97 + optionIndex)}) ${option}`).join('\n') : '';
        return `${index + 1}. ${item.question}\n${options}\nAnswer: ${item.answer}`;
      })
      .join('\n\n');
  }

  return JSON.stringify(data, null, 2);
}

async function sendRequest(endpoint, inputId, outputId) {
  const input = document.getElementById(inputId);
  const output = document.getElementById(outputId);
  const value = input.value.trim();

  if (!value) {
    output.textContent = 'Please enter some input before generating a result.';
    return;
  }

  output.textContent = 'Loading...';

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildPayload(endpoint, value))
    });

    const data = await response.json();

    if (!response.ok) {
      output.textContent = data.detail || 'Something went wrong.';
      return;
    }

    output.textContent = formatResult(data);
  } catch (error) {
    output.textContent = 'Network error. Please try again.';
  }
}
