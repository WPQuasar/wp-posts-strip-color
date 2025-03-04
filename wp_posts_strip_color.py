from bs4 import BeautifulSoup
import mysql.connector
import argparse

def remove_color_attributes(html):
    soup = BeautifulSoup(html, "html.parser")
    modified_tags = []
    for tag in soup.find_all(style=True):
        styles = tag["style"].split(";")
        new_styles = [s for s in styles if not s.strip().startswith("color:")]
        if len(new_styles) != len(styles):
            modified_tags.append((str(tag), str(tag).replace(tag["style"], "".join(new_styles).strip())))
        tag["style"] = ";".join(new_styles).strip()
        if not tag["style"]:
            del tag["style"]
    return str(soup), modified_tags

def process_posts(db_config, apply_all):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT ID, post_content FROM wp_posts WHERE post_type='post'")
    posts = cursor.fetchall()
    
    for post in posts:
        post_id = post['ID']
        original_content = post['post_content']
        updated_content, modified_tags = remove_color_attributes(original_content)
        
        if original_content != updated_content:
            print(f"\nPost ID: {post_id}")
            print("Changes:")
            for before, after in modified_tags:
                print("Before:")
                print(before)
                print("After:")
                print(after)
            
            if apply_all:
                cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (updated_content, post_id))
                conn.commit()
                print("Update applied.")
            else:
                confirm = input("Apply change? (y/n): ")
                if confirm.lower() == 'y':
                    cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (updated_content, post_id))
                    conn.commit()
                    print("Update applied.")
                else:
                    print("Update skipped.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database username")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--apply-all", action="store_true", help="Apply all changes without prompting")
    args = parser.parse_args()
    
    db_config = {
        "host": args.host,
        "user": args.user,
        "password": args.password,
        "database": args.database
    }
    
    process_posts(db_config, args.apply_all)

