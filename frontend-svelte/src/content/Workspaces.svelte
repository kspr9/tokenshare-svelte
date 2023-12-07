<div>
    <h1>Workspaces</h1>

    <div class="ws-items-container">
        <div class="workspace-item">
            <p>WS1</p>
        </div>
        <div class="workspace-item">
            <p>WS2</p>
        </div>
        <div class="workspace-item">
            <!-- svelte-ignore a11y-invalid-attribute -->
            <a href="#" class="link-style">
                <div class="icon-plus app-clr"></div>
            </a>
        </div>
    </div>
</div>
<style>
    .workspace-item {
        background-color: #333;
        width: 10ch;
        padding: 2ch 0;
        border-radius: 5px;
    }
    .ws-items-container {
        display: flex;
        gap: 10px;
        box-sizing: border-box;
        
    }

    .workspace-item > a {
        position: relative;
        top: 0.5ch;
        left: 2.5ch;
    }
    .workspace-item:has(a):hover {
        border: #646cff solid 1px;
    }


    /* Plus Icon styling */
    .icon-plus {
        width: 47px;
        height: 47px;
    
        &.w25 {
            width: 25px;
            height: 25px;
            
            border-radius: 5px;
            
            &:after {
                width: 18px;
                height: 4px;
                left: 4px;
                top: 11px;
            }

            &:before {
                width: 4px;
                height: 18px;
                left: 11px;
                top: 4px;
            }
        }
        
        border-radius: 50px;
        
        position: relative;

        &.orange {
            background: #FD7901;
        }
        
        &.blue {
            background: #3498db;
        }

        &.app-clr {
            background: #333;
        }
        
        &:after, &:before {
            content: '';
            position: absolute;
            background: #646cff;
            -webkit-border-radius: 5px;
            -moz-border-radius: 5px;
            border-radius: 5px;
        }

        /* the vertical line */
        &:before {
            left:50%;
            top:4px; /* this defines how much black "border" there should be */
            bottom:4px;
            width:5px;
            transform:translateX(-50%);
        }

        /* the horizontal line */
        &:after {
            top:50%;
            left:4px;
            right:4px;
            height:5px;
            transform:translateY(-50%);
        }
        
    }


    
    
/* END Plus Icon styling */
</style>