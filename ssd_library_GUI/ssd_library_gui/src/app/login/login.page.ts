import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  usernameFC: FormControl = new FormControl('', Validators.required);
  passwordFC: FormControl = new FormControl('', Validators.required);

  loginFG: FormGroup = new FormGroup({
    username: this.usernameFC,
    password: this.passwordFC
  });


  constructor(private router: Router,
              private auth: AuthService) {}

  ngOnInit() {
  }

  logIn() {
    this.loginFG.markAllAsTouched();
    this.loginFG.updateValueAndValidity();

    if (this.loginFG.valid){
      this.auth.login(this.usernameFC.value, this.passwordFC.value).subscribe(
        data => {
          this.router.navigate(['/home']);
          this.passwordFC.setValue('');
        },
        error => {
          console.log(error);
        }
      );
    }
  }

}
