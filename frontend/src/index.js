// import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Page404 from './404';
import './components/CustomAntd.css';
import "./components/CustomHtml.css";
import './components/component.css';
import CompanyDashBoard from './components/js/CompanyDashBoard';
import Permissions from './components/js/Permissions';
import QrBatch from './components/js/QrBatch';
import QrCode from './components/js/QrCode';
import SystemParameter from './components/js/SystemParameter';
import TaskScheduler from './components/js/TaskScheduler';
import UserWallet from './components/js/UserWallet';
import UsersWalletReport from './components/js/UsersWalletReport';
import Dashboard from './components/js/dashboard';
import Login from './components/js/login';
import Profile from './components/js/profile';
import Register from './components/js/register';
import User from './components/js/user';
import AuthProvider from './context/AuthContext';
import './index.css';
import reportWebVitals from './reportWebVitals';
import PrivateRoute from './utils/PrivateRoute';

const AuthRoute = ({component, code}) => {
  var main_menu = JSON.parse(localStorage.getItem("main_menu"))
  var auth_route = main_menu.map((data) => data["code"])
  if(auth_route.includes(code)){
    return component
  }else{
    return <Page404 />
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
      <Routes>
        <Route>
          <Route element={<AuthProvider  />}>
            <Route  element={<PrivateRoute  />}>
              <Route path="/" element={<Dashboard />}>

                    {/* nested page */}
                    <Route path="profile"              element={<Profile/>} />

                    {/* main menu page */}
                    <Route path="company_dashboard"    element={<AuthRoute component={<CompanyDashBoard/>}  code="company_dashboard" />} />
                    <Route path="user"                 element={<AuthRoute component={<User/>}              code="user" />} />
                    <Route path="user/user_wallet/:user_id"  element={<AuthRoute component={<UserWallet/>}  code="user"/> } />
                    <Route path="qr_batch"             element={<AuthRoute component={<QrBatch/>}           code="qr_batch" />} />
                    <Route path="qr_code"              element={<AuthRoute component={<QrCode/>}            code="qr_code" />} />
                    <Route path="users_wallet_report/" element={<AuthRoute component={<UsersWalletReport/>} code="users_wallet_report" />} />
                    <Route path="permissions/"         element={<AuthRoute component={<Permissions/>}       code="permissions" />} />
                    <Route path="system_parameter/"    element={<AuthRoute component={<SystemParameter/>}   code="system_parameter" />} />
                    <Route path="task_scheduler/"      element={<AuthRoute component={<TaskScheduler/>}   code="task_scheduler" />} />

                    {/* catch-all route for 404 page */}
                    <Route path="*" element={<Page404 />} />
              </Route>
            </Route>
            <Route path="/login" element={<Login />} />
          </Route>
          <Route path="/register" element={<Register />} />
        </Route>
      </Routes>
  </BrowserRouter>
);

reportWebVitals();
