import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  error = false;
  registrationError;
  showLogin = true;

  usernameLFC: FormControl = new FormControl('',
    [Validators.required,
    Validators.minLength(2),
    Validators.maxLength(20),
    Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);
  passwordLFC: FormControl = new FormControl('',
    [Validators.required,
      Validators.minLength(2),
      Validators.maxLength(20),
      Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);

  emailRFC: FormControl = new FormControl('',
    [Validators.required,
      Validators.minLength(5),
      Validators.maxLength(20),
      Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+@[a-zA-Z0-9\_\!\?\%\&\$]+\.[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);
  usernameRFC: FormControl = new FormControl('',
    [Validators.required,
      Validators.minLength(2),
      Validators.maxLength(20),
      Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);
  passwordRFC1: FormControl = new FormControl('',
    [Validators.required,
      Validators.minLength(2),
      Validators.maxLength(20),
      Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);
  passwordRFC2: FormControl = new FormControl('',
    [Validators.required,
      Validators.minLength(2),
      Validators.maxLength(20),
      Validators.pattern('^[a-zA-Z0-9\.\_\!\?\%\&\$]+$')]);

  loginFG: FormGroup = new FormGroup({
    username: this.usernameLFC,
    password: this.passwordLFC
  });

  registerFG: FormGroup = new FormGroup({
    email: this.emailRFC,
    username: this.usernameRFC,
    password1: this.passwordRFC1,
    password2: this.passwordRFC2
  }, { validators: this.passwordConfirming});


  constructor(private router: Router,
              private auth: AuthService) {}

  ngOnInit() {
  }

  logIn() {
    this.loginFG.markAllAsTouched();
    this.loginFG.updateValueAndValidity();

    if (this.loginFG.valid){
      this.auth.login(this.usernameLFC.value, this.passwordLFC.value).subscribe(
        data => {
          this.router.navigateByUrl('/home', {replaceUrl: true});
          this.loginFG.reset();
        },
        error => {
          this.error = true;
        }
      );
    }
  }

  register(){
    this.registerFG.markAllAsTouched();
    this.registerFG.updateValueAndValidity();

    if (this.registerFG.valid){
      this.auth.register(this.usernameRFC.value, this.emailRFC.value, this.passwordRFC1.value).subscribe(
        data => {
          this.router.navigateByUrl('/home', {replaceUrl: true});
          this.registerFG.reset();
        },
        error => {
          if(error.error.email[0] !== ''){
            this.registrationError = error.error.email[0];
          }else if(error.error.username[0] !== ''){
            this.registrationError = error.error.username[0];
          }else if(error.error.password1[0] !== ''){
            this.registrationError = error.error.password1[0];
          }
          this.error = true;
        }
      );
    }
  }

  passwordConfirming(c: AbstractControl): { invalid: boolean } {
    if (c.get('password1').value !== c.get('password2').value) {
      return {invalid: true};
    }
  }
}
