import { QrcodeOutlined } from "@ant-design/icons";
import { Button, Input, Modal, QRCode, Table } from "antd";
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import useAxios from "../../utils/useAxios";

export default function QrCode(){
    const api = useRef(useAxios())
    const { Search } = Input;
    const [QRCodeData , setQRCodeData] = useState([])
    const [totalRecord , setTotalRecord] = useState(0)
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [selectedRows ,setSelectedRows] = useState([])
    const {messageApi} = useContext(AuthContext)
    const [filterDict, setFilterDict] = useState({page:1,pageSize:10,orderBy:"-id",search:"",is_used:""})
    const [isUsed, setIsUsed] = useState({used:true, un_used:true})

    let getQRCodeData = useCallback(async()=>{
        await api.current.get(`/qr_admin/qr_code_list/?page=${filterDict.page}&page_size=${filterDict.pageSize}&ordering=${filterDict.orderBy}&search=${filterDict.search}&is_used=${filterDict.is_used}`)
        .then((res)=>{
            setTotalRecord(res.data.count)
            setQRCodeData(res.data.results)
        })
        .catch((error)=>{
            messageApi.open({type: 'error',content: error.message})
        })
    },[filterDict, messageApi])

    useEffect(()=>{
        getQRCodeData()
    },[getQRCodeData])


    const onSelectChange =(newSelectedRowKeys, selectedRows)=>{
        setSelectedRows(selectedRows)
        setSelectedRowKeys(newSelectedRowKeys)
    }

    const onTableChange = (pagination, filters, sorter) =>{
        var orderBy = sorter.order ? (sorter.order === "ascend"? "":"-") + sorter.field : "-id"
        setFilterDict({...filterDict,page:pagination.current,pageSize:pagination.pageSize,orderBy:orderBy})
    }
    const openQRCode = (qr_code) =>{
         Modal.info({
            title: `QR Code`,
            content: (<><div style={{padding: '4% 23%'}}><QRCode size={150} type="svg" value={qr_code}/></div><div>{qr_code}</div></>),
            onOk() {},
        })

    }
    const onCheckUsed= (e) =>{
        let used = document.getElementById("used").checked
        let un_used = document.getElementById("un_used").checked
        var is_used = (un_used && !used) ? "False" : (!un_used && used) ? "True" : "";
        setIsUsed({...isUsed,[e.target.id]:e.target.checked,is_used:is_used})
        setFilterDict({...filterDict,page:1,is_used:is_used})
    }

    const columns = [
        {title:"QR Number",dataIndex:"qr_number",sorter: true},
        {title:"QR Code",dataIndex:"qr_code", width: '30%',sorter: true},
        {title:"Batch Number",dataIndex:"batch__batch_number",sorter: true},
        {title:"Point",dataIndex:"point",sorter: true, width: 100},
        {
            title:"Disabled",
            dataIndex:"is_disabled",
            sorter: true,
            width: 100,
            render:(is_disabled)=>{return is_disabled ? <i className="fa fa-check"></i> :""}
        },
        {title:"Used On",dataIndex:"used_on",sorter: true},
        {title:"Used By",dataIndex:"used_by__mobile",sorter: true},
        {title:"View QR",
            dataIndex:"qr_code",
            render:(qr_code)=>(<Button type='primary'
            onClick={()=>openQRCode(qr_code)} size='small' icon={<QrcodeOutlined />}>View QR</Button>)
        }
    ]

    const enableDisableQR = async(status)=>{
        if(selectedRowKeys.length <= 0){
            messageApi.open({type: 'error',content: "Please select at least one qr code."});
            return
        }
        else{
            if (status === "disable"){
                var un_used = selectedRows.filter((item) => item.used_on != null)
                if (un_used.length > 0){
                    messageApi.open({type: 'error',content: "Used QR code can not be disable."})
                    return
                }
            }
            await api.current.post(`/qr_admin/disable_qr_code/`,{selectedRowKeys:selectedRowKeys,status:status})
            .then((res)=>{
                getQRCodeData()
                setSelectedRowKeys([]);
                messageApi.open({type: 'success',content: res.data.message})
            })
            .catch((error)=>{
                messageApi.open({type: 'error',content: error.message})
            })
        }
    }
    return(
        <>
        <div className='title_tab'>
            <div className='title_tab_title'>QR Code</div>
            <div className="title_tab_div">
              <Search placeholder="Search by Qr Number, Batch number" allowClear={true} onChange={(e)=> {if(e.target.value===""){setFilterDict({...filterDict, search:""})}}} onSearch={(value) => setFilterDict({...filterDict, search:value})} style={{ width: 200 }} />
               <Button type="primary" onClick={()=>enableDisableQR("disable")}>Disable QR</Button>
               <Button type="primary" onClick={()=>enableDisableQR("enable")}>Enable QR</Button>
            </div>
        </div>
        <div className='report_tab'>
              <div style={{fontSize: 'medium'}}>
                <label><input type="checkbox" id="used" onChange={onCheckUsed} checked={isUsed.used}/>Used Code</label>&nbsp;
                <label><input type="checkbox" id="un_used" onChange={onCheckUsed} checked={isUsed.un_used}/>Unused Code</label>
              </div>
        </div>
        <div className='main_tab'>
            <Table
                columns={columns}
                dataSource={QRCodeData} rowKey="id"
                onChange={onTableChange}
                rowSelection={{selectedRowKeys,onChange: onSelectChange}}
                pagination={{total: totalRecord,
                    defaultPageSize: filterDict.pageSize,
                    current: filterDict.page,
                    showSizeChanger: true,
                    pageSizeOptions: ['10', '20', '50', '100'],
                }}
                footer={() => ( <div style={{textAlign:'right'}}>Selected Records ({selectedRowKeys.length} of {totalRecord})</div>)}
                scroll={{ x: '75pc' }}
                size="small"/>
        </div>
        </>
    )
}