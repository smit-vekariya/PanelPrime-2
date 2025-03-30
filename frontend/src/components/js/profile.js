import { Button, Form, Input } from 'antd';
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import useAxios from "../../utils/useAxios";
import '../component.css';

export default function Profile(){
    const api = useRef(useAxios())
    const [profile, setProfile] = useState({})
    const {messageApi} = useContext(AuthContext)
    const[disabled, setDisabled] = useState(true)


    const getProfileData = useCallback(async() =>{
        await api.current.get('/account/user_profile/')
        .then((res)=>{
            if(res.data.status === 1){
                setProfile(res.data.data[0][0])
            }
            else{
                messageApi.open({type: 'error',content: res.data.message})
            }
        })
        .catch((error)=>{
            messageApi.open({type: 'error',content: error.message})
        })
    },[messageApi])

    useEffect(()=>{
        getProfileData()
    },[getProfileData])

    const editProfile=(e)=>{
        setProfile({...profile,[e.target.name]:e.target.value})
    }
    const saveProfile = async() =>{
        await api.current.put(`/account/edit_profile/${profile.id}`,profile)
            .then((res)=>{
                if(res.data.status ===1){
                    setDisabled(true)
                    messageApi.open({type: 'success',content: res.data.message})
                }
                else{
                    messageApi.open({type: 'error',content: res.data.message})
                }
            })
            .catch((error)=>{
                messageApi.open({type: 'error',content: error.message})
            })
    }


     return (
        <>
        <div className='title_tab'>
            <div className='title_tab_title'>Profile</div>
        </div>
        <div className='main_tab'>
            <Form  style={{ maxWidth: 600,margin: '19px 6px'}}  labelCol={{flex: '110px'}} labelAlign="left">
                <Form.Item label="Full Name">
                    <Input type='text' className='edit' name="full_name" onChange={editProfile} value={profile.full_name} disabled={disabled}></Input>
                </Form.Item>
                <Form.Item label="Mobile No.">
                    <Input type='text' className='edit' name ="mobile" onChange={editProfile} value={profile.mobile} disabled={disabled}></Input>
                </Form.Item>
                <Form.Item label="Address">
                    <Input type='text' className='edit' name="address" onChange={editProfile} value={profile.address} disabled={disabled}></Input>
                </Form.Item>
                <Form.Item label="Pin Code">
                    <Input type='text' className='edit' name="pin_code" onChange={editProfile} value={profile.pin_code} disabled={disabled}></Input>
                </Form.Item>
                <Form.Item label="City">
                    <Input type='text' value={profile.city} disabled></Input>
                </Form.Item>
                <Form.Item label="State">
                    <Input type='text' value={profile.state} disabled></Input>
                </Form.Item>
            </Form>
            <div>
                {disabled ?
                <Button type="primary" onClick={()=>setDisabled(false) }>Edit Profile</Button>
                 : <><Button type="primary" onClick={saveProfile}>Save Profile</Button>&nbsp;<Button onClick={()=>setDisabled(true) }>Cancel</Button></>}
            </div>
        </div>
        </>
    )
}