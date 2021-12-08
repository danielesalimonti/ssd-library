import {Component, HostListener, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  emailFC: FormControl = new FormControl('', Validators.required);
  passwordFC: FormControl = new FormControl('', Validators.required);

  loginFG: FormGroup = new FormGroup({
    email: this.emailFC,
    password: this.passwordFC
  });


  constructor(private router: Router) {

  }

  ngOnInit() {
  }

  logIn() {
    this.loginFG.markAllAsTouched();
    this.loginFG.updateValueAndValidity();
    if (this.loginFG.valid && this.emailFC.value === 'admin' && this.passwordFC.value === 'admin') {
      this.router.navigate(['/home']);
    }
  }

}
