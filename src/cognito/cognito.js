import { Config, CognitoIdentityCredentials } from 'aws-sdk'
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute
} from 'amazon-cognito-identity-js'

export default class Cognito {
  configure (config) {
    if (config.userPool) {
      this.userPool = config.userPool
    } else {
      this.userPool = new CognitoUserPool({
        UserPoolId: config.UserPoolId,
        ClientId: config.ClientId
      })
    }
    Config.region = config.region
    Config.credentials = new CognitoIdentityCredentials({
      IdentityPoolId: config.IdentityPoolId
    })
    this.options = config
  }

  static install = (Vue, options) => {
    Object.defineProperty(Vue.prototype, '$cognito', {
      get () { return this.$root._cognito }
    })

    Vue.mixin({
      beforeCreate () {
        if (this.$options.cognito) {
          this._cognito = this.$options.cognito
          this._cognito.configure(options)
        }
      }
    })
  }

  /*
    username, passwordでサインアップ
    username = emailとしてUserAttributeにも登録
   */
  signUp (username, password) {
    const dataEmail = { Name: 'email', Value: username }
    const attributeList = []

    attributeList.push(new CognitoUserAttribute(dataEmail))

    return new Promise((resolve, reject) => {
      this.userPool.signUp(username, password, attributeList, null, (err, result) => {
        if (err) {
          reject(err)
        } else {
          resolve(result)
        }
      })
    })
  }

  /*
    確認コードからユーザーを有効化する
   */
  confirmation (username, confirmationCode) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)

    return new Promise((resolve, reject) => {
      cognitoUser.confirmRegistration(confirmationCode, true, (err, result) => {
        if (err) {
          reject(err)
        } else {
          resolve(result)
        }
      })
    })
  }

  /*
   username, passwordでログイン
   */
  login (username, password) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)
    const authenticationData = { Username: username, Password: password }
    const authenticationDetails = new AuthenticationDetails(authenticationData)

    return new Promise((resolve, reject) => {
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (result) => {
          resolve(result)
        },
        onFailure: (err) => {
          reject(err)
        }
      })
    })
  }

  changePassword (oldPassword, newPassword) {
    var cognitoUser = this.userPool.getCurrentUser()
    return new Promise((resolve, reject) => {
      cognitoUser.getSession(function (err, result) {
        if (result) {
          cognitoUser.changePassword(oldPassword, newPassword, (err, result) => {
            if (err) {
              reject(err)
            } else {
              resolve(result)
            }
          })
        } else {
          reject(err)
        }
      })
    })
  }

  forgotPassword (username) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)
    return new Promise((resolve, reject) => {
      cognitoUser.forgotPassword({
        onSuccess: (result) => {
          resolve(result)
        },
        onFailure: (err) => {
          reject(err)
        }
      })
    })
  }

  confirmForgotPassword (username, confirmationCode, newPassword) {
    const userData = { Username: username, Pool: this.userPool }
    const cognitoUser = new CognitoUser(userData)
    return new Promise((resolve, reject) => {
      cognitoUser.confirmPassword(confirmationCode, newPassword, {
        onSuccess: (result) => {
          resolve(result)
        },
        onFailure: (err) => {
          reject(err)
        }
      })
    })
  }

  delete () {
    var cognitoUser = this.userPool.getCurrentUser()
    return new Promise((resolve, reject) => {
      cognitoUser.getSession(function (err, result) {
        if (result) {
          cognitoUser.deleteUser((err, result) => {
            if (err) {
              reject(err)
            } else {
              resolve(result)
            }
          })
        } else {
          reject(err)
        }
      })
    })
  }

  /*
    ログアウト
   */
  logout () {
    this.userPool.getCurrentUser().signOut()
  }

  /*
    ログインしているかの判定
   */
  isAuthenticated () {
    const cognitoUser = this.userPool.getCurrentUser()
    return new Promise((resolve, reject) => {
      if (cognitoUser === null) { reject(cognitoUser) }
      cognitoUser.getSession((err, session) => {
        if (err) {
          reject(err)
        } else {
          if (!session.isValid()) {
            reject(session)
          } else {
            resolve(session)
          }
        }
      })
    })
  }
}
