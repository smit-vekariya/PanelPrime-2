import { Button, Card, Form, Input } from 'antd';
import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import logo from '../images/logo-no-background.png';

export default function  Login(){
    const {loginUser} = useContext(AuthContext)
    return(
        <>
            <div className="main_div">
                <div className="login_div">
                    <div style={{margin: '22px'}}>
                        <img src={logo} alt="logo-no-background.png" style={{width:"300px"}}></img>
                    </div>
                    <Card title="LOGIN" className='login_card' bordered={true}>
                        <Form name="basic" labelCol={{flex: '110px'}} labelAlign="left" wrapperCol={{span: 16,}}style={{maxWidth: 600}}
                            initialValues={{remember: true,}} onFinish={loginUser} autoComplete="off">
                            <Form.Item label="Mobile" name="mobile" rules={[{required: true, message: 'Please input your mobile number!',},]}>
                                <Input />
                            </Form.Item>
                            <Form.Item label="Password" name="password" rules={[{required: true, message: 'Please input your password!',},]}>
                                <Input.Password />
                            </Form.Item>
                            <Form.Item style={{ margin: '2px 188px'}}>
                                <Button type="primary" htmlType="submit">Submit</Button>
                            </Form.Item>
                        </Form>
                    </Card>
                </div>
            </div>
        </>
    )
}