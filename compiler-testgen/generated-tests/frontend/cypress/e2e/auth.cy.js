
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
