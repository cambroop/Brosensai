import streamlit as st
import math
import pandas as pd
from collections import Counter

st.write("===โปรแกรมคำนวณค่าสถิติ ===")
st.write("**กรอกข้อมูล (เฉพาะค่าบวก ระหว่าง 1-999 **")
st.write("หยุดเมื่อกด Enter หรือ พิมพ์ 'stop'")

if 'data' not in st.session_state:
    st.session_state.data = []
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = ""
if 'warning_msg' not in st.session_state:
    st.session_state.warning_msg = ""

def add_data():
    val_str = st.session_state.user_input_box
    st.session_state.error_msg = ""
    st.session_state.warning_msg = ""
    
    if val_str == '' or val_str == 'stop':
        st.session_state.warning_msg = "สิ้นสุดการกรอกข้อมูล"
    else:
        try:
            val = int(val_str)
            if 1 <= val <= 999:
                st.session_state.data.append(val)
            else:
                st.session_state.error_msg = "กรอกเฉพาะค่าระหว่าง 1 ถึง 999 เท่านั้น"
        except ValueError:
            st.session_state.error_msg = "กรอกเฉพาะตัวเลข"
            
    st.session_state.user_input_box = ""

# --- เพิ่มส่วน Import ไฟล์ข้อมูล (รองรับทั้ง Text, CSV และ Excel) ---
st.markdown("---")
uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ข้อมูล (รองรับไฟล์ .txt, .csv, .xlsx)", type=["txt", "csv", "xlsx", "xls"])
if uploaded_file is not None:
    try:
        loaded_data = []
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension in ['xlsx', 'xls']:
            # อ่านไฟล์ Excel ด้วย pandas
            df = pd.read_excel(uploaded_file)
            # ดึงข้อมูลทุกแถว ทุกคอลัมน์ที่เป็นตัวเลข
            for col in df.columns:
                for val in df[col].dropna():
                    try:
                        v = int(val)
                        if 1 <= v <= 999:
                            loaded_data.append(v)
                    except ValueError:
                        pass
        else:
            # อ่านไฟล์ Text หรือ CSV ปกติ
            content = uploaded_file.read().decode("utf-8")
            tokens = content.replace(',', ' ').split()
            for t in tokens:
                v = int(t)
                if 1 <= v <= 999:
                    loaded_data.append(v)
                    
        if loaded_data:
            st.session_state.data = loaded_data[:100]
            st.success(f"นำเข้าข้อมูลจากไฟล์สำเร็จ! ทั้งหมด {len(loaded_data)} ตัว")
        else:
            st.error("ไม่พบข้อมูลตัวเลขที่ถูกต้อง (ระหว่าง 1-999) ในไฟล์ที่อัปโหลด")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
st.markdown("---")

# แสดงคำเตือนไว้ด้านบนของช่องกรอกข้อมูล
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)
if st.session_state.warning_msg:
    st.warning(st.session_state.warning_msg)

# แบ่งคอลัมน์: ซ้ายเป็นช่องกรอกข้อมูล / ขวาเป็นปุ่มล้างข้อมูล
col_input, col_btn = st.columns([3, 1])

with col_input:
    st.text_input(f"ข้อมูลชิ้นที่ {len(st.session_state.data) + 1}:", key="user_input_box", on_change=add_data)

with col_btn:
    st.write("") # เว้นระยะให้ปุ่มอยู่ระดับเดียวกับช่องกรอก
    if st.button("ล้างข้อมูลทั้งหมด"):
        st.session_state.data = []
        st.session_state.error_msg = ""
        st.session_state.warning_msg = ""
        st.rerun()


st.write(f"รายการข้อมูลปัจจุบัน: {st.session_state.data}")
numclasses_input = st.text_input("กรอกจำนวนชั้น(อยู่ระหว่าง 3 - 15 ชั้น):", "5")

def data100():
    return st.session_state.data

def cus(data):
    if not data:
        st.write("ไม่มีข้อมูลสำหรับคำนวณ")
        return
    n = len(data)
    maxval = max(data)
    minval = min(data)
    meanval = sum(data) / n
    
    sorted_data = sorted(data)
    if n % 2 == 1:
        medianval = sorted_data[n // 2]
    else:
        medianval = (sorted_data[(n // 2) - 1] + sorted_data[n // 2]) / 2
        
    count = Counter(data)
    maxfreq = max(count.values())
    modes = [i for i, v in count.items() if v == maxfreq]
    modeval = modes if len(modes) > 1 else modes[0]

    sum_abs_diff = sum(abs(x - meanval) for x in data)
    mdval = sum_abs_diff / n

    if n > 1:
        sum_sq_diff = sum((x - meanval) ** 2 for x in data)
        varianceval = sum_sq_diff / (n - 1)
        sdval = math.sqrt(varianceval)
    else:
        varianceval = 0.0
        sdval = 0.0
        
    st.write("\n*** ผลการคำนวณข้อมูลไม่แจกแจงความถี่ ***")
    st.write(f"จำนวนข้อมูลทั้งหมด              : {n}")
    st.write(f"ข้อมูลเรียงลำดับ                 : {sorted_data}")
    st.write(f"ค่าสูงสุด                      : {maxval}")
    st.write(f"ค่าต่ำสุด                      : {minval}")
    st.write(f"ค่าเฉลี่ย                      : {meanval:.2f}")
    st.write(f"ค่ามัธยฐาน                    : {medianval}")
    st.write(f"ค่าฐานนิยม                    : {modeval}")
    st.write(f"ค่าความเบี่ยงเบนเฉลี่ย             : {mdval:.2f}")
    st.write(f"ส่วนเบี่ยงเบนมาตรฐาน             : {sdval:.2f}")
    st.write(f"ค่าความแปรปรวน                : {varianceval:.2f}")

def fdv(data):
    if not data:
        st.write("ไม่มีข้อมูลสำหรับคำนวณ")
        return
    n = len(data)
    maxval = max(data)
    minval = min(data)
    rangeval = maxval - minval
    st.write(f"\n*** ข้อมูลแจกแจงความถี่ ***")
    st.write(f"ค่าสูงสุด: {maxval}")
    st.write(f"ค่าต่ำสุด: {minval}")
    st.write(f"พิสัย = max - xin: {rangeval}")
    
    try:
        numclasses = int(numclasses_input)
    except ValueError:
        numclasses = 5

    if not (3 <= numclasses <= 15):
        st.write("กรุณากรอกจำนวนชั้นให้อยู่ในช่วง 3 ถึง 15 ชั้นเท่านั้น")
        return

    interval = math.ceil(rangeval / numclasses)
    if interval == 0:
        interval = 1
    st.write(f"ความกว้างอันตรภาคชั้น:{interval}")
    st.write("\n*** ตารางแจกแจงความถี่และค่าสถิติประจำชั้น ***")
    
    table_rows = []
    table_rows.append(f"{'ชั้นที่':<6} {'อันตรภาคชั้น':<15} {'ความถี่(f)':<10} {'ความถี่สะสม(F)':<15} {'สัดส่วน(f/N)':<15} {'ร้อยละ(%)':<10}")
    table_rows.append("*" * 70)
    
    lowerbound = minval
    Cumulativefrequency = 0

    for i in range(1, numclasses + 1):
        upperbound = lowerbound + interval - 1
        freq = sum(1 for m in data if lowerbound <= m <= upperbound)
        Cumulativefrequency += freq
        proportion = freq / n
        percentage = (freq / n) * 100
        table_rows.append(f"{i:<6} {f'{lowerbound} - {upperbound}':<13} {freq:<10} {Cumulativefrequency:<9} {proportion:<10.4f} {percentage:<10.2f}")
        lowerbound = upperbound + 1
        
    for row in table_rows:
        st.text(row)

if st.button("คำนวณผลลัพธ์ทั้งหมด"):
    rew_data = data100()
    cus(rew_data)
    fdv(rew_data)
