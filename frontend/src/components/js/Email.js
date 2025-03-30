import { Button, Modal,Input, Form } from 'antd';
import React, {useState, useRef, useCallback, useContext } from 'react';
import useAxios from '../../utils/useAxios';
import { AuthContext } from "../../context/AuthContext";


const EMAIL_FROM = process.env.REACT_APP_EMAIL_FROM
export default function Email(){
    const api = useRef(useAxios())
    const {messageApi} = useContext(AuthContext)
    const { TextArea } = Input;
    var mail_data = {"is_now":true,"to":"","cc":"","bcc":"","subject":"","body":""}
    const [mailData, setMailData] = useState(mail_data)
    const [isModalOpen, setIsModalOpen] = useState(false);

    const onSend = useCallback(async() =>{
        await api.current.post('/post_office/send_mail/',{
            "mail_data":mailData
        }).then((res)=>{
            if(res.data.status === 0){
                messageApi.open({type: 'error',content: res.data.message})
            }else{
                messageApi.open({type: 'success',content: res.data.message})
                setIsModalOpen(false)
            }
        }).catch((error)=>{
            messageApi.open({type:'error', content:error.message})
        })

    },[messageApi, mailData])

    const onMailData = (e) =>{
        setMailData({...mailData, [e.target.name]: e.target.value})
    }

    return (
        <>
        <Button style={{marginLeft: '10px'}} type="dashed" onClick={()=> {setIsModalOpen(true); setMailData(mail_data)}}>Send Mail</Button>

        <Modal title="Send Mail" width={1200} style={{ top: 20 }} open={isModalOpen} okText="Send"  footer={[
            <Button onClick={()=>setIsModalOpen(false)}>Cancel</Button>,
            <Button form="myForm" type="primary" key="submit" htmlType="submit">Send</Button>]} onCancel={()=>setIsModalOpen(false)}>
            <Form id="myForm" onFinish={onSend}>
               <div>
                <Input addonBefore="From" className='mail_input' value={EMAIL_FROM} disabled />
                <Input addonBefore="To" className='mail_input' name="to" onChange={onMailData} value={mailData.to} required/>
                <Input addonBefore="Cc" className='mail_input' name="cc"  onChange={onMailData} value={mailData.cc} />
                <Input addonBefore="Bcc" className='mail_input' name="bcc"  onChange={onMailData} value={mailData.bcc} />
                <Input addonBefore="Subject" className='mail_input'name="subject"   onChange={onMailData} value={mailData.subject} required/>
                    <div style={{margin: '0px 5px'}}> 
                        <TextArea
                            showCount
                            name="body"
                            onChange={onMailData}
                            className='mail_body'
                            value={mailData.body}
                            maxLength={1000}
                            style={{ height: 400}}
                            required
                            />
                    </div>
                <label><input type="checkbox" checked={mailData.is_now} onChange={(e)=> setMailData({...mailData, is_now:e.target.checked }) }/>Send Now</label>
               </div>
            </Form>
        </Modal>
        </>
    )
}