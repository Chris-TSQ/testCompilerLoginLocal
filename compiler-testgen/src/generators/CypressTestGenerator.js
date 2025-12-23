const TestGenerator = require("./TestGenerator");

class CypressTestGenerator extends TestGenerator {
  supports(filePath) {
    return filePath.endsWith(".js") || filePath.endsWith(".html");
  }

  generate() {
    const testCode = `
describe('Auth flow', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('shows validation error', () => {
    cy.get('#signup-btn').click()
    cy.contains('All fields are required')
  })

  it('logs in successfully', () => {
    cy.intercept('POST', '/api/login', {
      statusCode: 200,
      body: { token: 'token', username: 'test' }
    })

    cy.get('#loginUsername').type('test')
    cy.get('#loginPassword').type('123')
    cy.get('#login-btn').click()

    cy.contains('test')
  })
})
`;

    this.writeFile(
      `frontend/cypress/e2e/auth.cy.js`,
      testCode
    );
  }
}

module.exports = CypressTestGenerator;
