import { Button, Input, Table, Tag } from 'antd';
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from '../../context/AuthContext';
import useAxios from "../../utils/useAxios";


export default function User(){
    const api = useRef(useAxios())
    const { Search } = Input;
    const [users, setUsers] = useState([])
    const [totalRecord , setTotalRecord] = useState(0)
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const {messageApi} = useContext(AuthContext)
    const [filterDict, setFilterDict] =useState({page:1,pageSize:10,orderBy:"-id",search:""})


    let getUserData = useCallback(async () =>{
        await api.current.get(`/qr_admin/user_list/?page=${filterDict.page}&page_size=${filterDict.pageSize}&ordering=${filterDict.orderBy}&search=${filterDict.search}`,
            )
            .then((res)=>{
                setTotalRecord(res.data.count)
                setUsers(res.data.results)
            })
            .catch((error)=>{
                messageApi.open({type: 'error',content: error.message})
            })
    },[filterDict, messageApi])

    useEffect(()=>{
        getUserData();
    }, [getUserData])


    const columns = [
        {title:"First Name",dataIndex:"first_name",sorter: true},
        {title:"Last name",dataIndex:"last_name",sorter: true},
        {title:"Email",dataIndex:"email",sorter: true},
        {title:"Is active",dataIndex:"is_active", sorter: true,
            render: (is_active) => {
                const color = is_active ? 'green' : 'volcano';
                const tag = is_active ? 'Active' : 'Inactive';

                return (
                <Tag color={color} key={tag}>
                    {tag.toUpperCase()}
                </Tag>
                );
            }
        },
        {title:"Last Login",dataIndex:"last_login", sorter: true},
        {title:"Group", dataIndex:"group__name", sorter: true},
    ]

    const onSelectChange =(newSelectedRowKeys)=>{
        setSelectedRowKeys(newSelectedRowKeys)
    }

    const onTableChange = (pagination, filters, sorter) =>{
        var orderBy = sorter.order ? (sorter.order === "ascend"? "":"-") + sorter.field : "-id"
        setFilterDict({...filterDict,page:pagination.current,pageSize:pagination.pageSize,orderBy:orderBy})
    }

    return(
    <>
       <div className='title_tab'>
            <div className='title_tab_title'>Users</div>
            <div className="title_tab_div">
                <Search placeholder="Search by name, email" allowClear={true} onChange={(e)=> {if(e.target.value===""){setFilterDict({...filterDict, search:""})}}} onSearch={(value) => setFilterDict({...filterDict, search:value})} style={{ width: 200 }} />
            </div>
        </div>
        <div className='main_tab'>
        <Table
            columns={columns}
            dataSource={users} rowKey="id"
            onChange={onTableChange}
            rowSelection={{selectedRowKeys,onChange: onSelectChange}}
            pagination={{total: totalRecord,
                defaultPageSize: 10, showSizeChanger: true,
                pageSizeOptions: ['10', '20', '50', '100'],
            }}
            footer={() => ( <div style={{textAlign:'right'}}>Selected Records ({selectedRowKeys.length} of {totalRecord})</div>)}
            scroll={{ x: '75pc' }}
            size="small"/>
        </div>
    </>
    )
}
